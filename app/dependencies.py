from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_app import get_redis
from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from app.database import get_db
from app.exceptions.user_exception import UserNotFoundError
from app.models.user import UserORM
from app.repositories.redis_repo import RedisRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.comment_service import CommentService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

security = HTTPBearer()


async def get_uow_factory(db: AsyncSession = Depends(get_db)) -> UnitOfWork:
    return UnitOfWork(session=db)


def get_redis_repo(
    redis: Redis = Depends(get_redis),
) -> RedisRepository:
    return RedisRepository(redis=redis)


async def get_auth_service(
    uow: UnitOfWork = Depends(get_uow_factory),
    redis: Redis = Depends(get_redis),
    redis_repo: RedisRepository = Depends(get_redis_repo),
) -> AuthService:
    return AuthService(
        uow=uow,
        token_repo=RefreshTokenRepository(redis=redis),
        redis_repo=redis_repo,
    )


async def get_project_services(
    uow: UnitOfWork = Depends(get_uow_factory),
) -> ProjectService:
    return ProjectService(uow=uow)


async def get_task_service(uow: UnitOfWork = Depends(get_uow_factory)) -> TaskService:
    return TaskService(uow=uow)


async def get_comment_service(
    uow: UnitOfWork = Depends(get_uow_factory),
) -> CommentService:
    return CommentService(uow=uow)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> UserORM:
    token = credentials.credentials
    repo = UserRepository(session=db)
    user_id = decode_access_token(token)
    user = await repo.get_by_id(user_id=user_id)
    if not user:
        raise UserNotFoundError()
    return user
