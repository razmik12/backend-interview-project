import asyncio
import hmac
import uuid

from fastapi import Response
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.core.security import (
    DUMMY_HASH,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.core.uow import UnitOfWork
from app.exceptions.general_exception import LockAcquisitionError
from app.exceptions.user_exception import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.models.user import UserORM
from app.repositories.redis_repo import RedisRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.schemas.user import TokenResponse, UserCreate, UserLogin


class AuthService:
    def __init__(
        self,
        uow: UnitOfWork,
        token_repo: RefreshTokenRepository,
        redis_repo: RedisRepository,
    ):
        self.uow = uow
        self.token_repo = token_repo
        self.redis_repo = redis_repo

    async def register(self, data: UserCreate) -> UserORM:
        async with self.uow as uow:
            if await uow.user_repo.get_by_email(data.email):
                raise EmailAlreadyExistsError()
            try:
                hashed = await asyncio.to_thread(hash_password, password=data.password)

                return await uow.user_repo.create_user(
                    email=data.email,
                    hashed_password=hashed,
                    full_name=data.full_name,
                )
            except IntegrityError:
                raise EmailAlreadyExistsError()

    def _set_refresh_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(
            key="refresh_token",
            value=token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            path="/auth",
            max_age=settings.refresh_exp * 24 * 60 * 60,
        )

    async def login(
        self, data: UserLogin, response: Response, ip_address: str
    ) -> TokenResponse:
        await self.redis_repo.rate_limiting(identifier=ip_address, ttl=60, limit=5)
        async with self.uow as uow:
            user = await uow.user_repo.get_by_email(email=data.email)
            if not user:
                await asyncio.to_thread(
                    verify_password, password=data.password, hashed_password=DUMMY_HASH
                )
                raise InvalidCredentialsError()

            if not await asyncio.to_thread(
                verify_password,
                password=data.password,
                hashed_password=user.hashed_password,
            ):
                raise InvalidCredentialsError()

            session_id = uuid.uuid4()

            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id, session_id)

            self._set_refresh_cookie(response, refresh_token)

            await self.token_repo.set_token(
                token=hash_token(refresh_token),
                user_id=user.id,
                session_id=session_id,
                ttl=settings.refresh_exp * 24 * 60 * 60,
            )

            return TokenResponse(
                access_token=access_token,
            )

    async def refresh_access_token(
        self, refresh_token: str | None, response: Response
    ) -> TokenResponse:
        if not refresh_token:
            raise InvalidCredentialsError()

        payload = decode_refresh_token(token=refresh_token)
        async with self.uow as uow:
            user = await uow.user_repo.get_by_id(user_id=payload.sub)

            if not user:
                raise UserNotFoundError()

            lock_token = await self.redis_repo.acquire_lock(
                session_id=payload.session_id, ttl=5
            )

            if not lock_token:
                raise LockAcquisitionError()

            try:
                token = await self.token_repo.get_token(
                    user_id=user.id, session_id=payload.session_id
                )

                if not token:
                    raise InvalidCredentialsError()
                if not hmac.compare_digest(token, hash_token(refresh_token)):
                    raise InvalidCredentialsError()

                new_access_token = create_access_token(user_id=user.id)
                new_refresh_token = create_refresh_token(
                    user_id=user.id, session_id=payload.session_id
                )

                await self.token_repo.set_token(
                    token=hash_token(new_refresh_token),
                    user_id=user.id,
                    session_id=payload.session_id,
                    ttl=settings.refresh_exp * 24 * 60 * 60,
                )

            finally:
                await self.redis_repo.release_lock(
                    token=lock_token, session_id=payload.session_id
                )

        self._set_refresh_cookie(response, new_refresh_token)

        return TokenResponse(access_token=new_access_token)

    async def logout(self, token: str | None, response: Response):
        if token is None:
            raise InvalidCredentialsError()
        async with self.uow as uow:
            payload = decode_refresh_token(token=token)

            if not await uow.user_repo.get_by_id(user_id=payload.sub):
                raise InvalidCredentialsError()

            stored_token = await self.token_repo.get_token(
                user_id=payload.sub, session_id=payload.session_id
            )

            if not stored_token:
                raise InvalidCredentialsError()

            if not hmac.compare_digest(stored_token, hash_token(token)):
                raise InvalidCredentialsError()

            await self.token_repo.delete_token(
                user_id=payload.sub, session_id=payload.session_id
            )

            response.delete_cookie(key="refresh_token", path="/auth")
