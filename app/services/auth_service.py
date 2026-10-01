from fastapi import Response
from jose import jwt,JWTError
from app.models.user import UserORM
from app.schemas.user import UserCreate,UserLogin,TokenResponse
from app.exceptions.user_exception import EmailAlreadyExistsError,InvalidCredentialsError, UserNotFoundError
from app.core.security import decode_refresh_token, verify_password,hash_password
from app.core.uow import UnitOfWork
from sqlalchemy.exc import IntegrityError
from app.core.security import create_access_token,create_refresh_token
from app.config import settings

class AuthService:
    def __init__(self,uow:UnitOfWork):
        self.uow = uow

    
    async def register(self,data:UserCreate)->UserORM:
        async with self.uow as uow:     
            if await uow.user_repo.get_by_email(data.email):
                raise EmailAlreadyExistsError()
            try:
               return await uow.user_repo.create_user(email=data.email, hashed_password=hash_password(data.password),full_name=data.full_name)
            except IntegrityError:
               raise EmailAlreadyExistsError()
           
    async def login(self,data:UserLogin,response:Response)->TokenResponse:
        async with self.uow as uow:
            user = await uow.user_repo.get_by_email(email=data.email)
            if not user:
                raise InvalidCredentialsError()
            if not verify_password(password=data.password,hashed_password=user.hashed_password):
                raise InvalidCredentialsError()
            
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            
            response.set_cookie(key="refresh_token",
                                value=refresh_token,
                                httponly=True,
                                secure=False,
                                max_age=7 * 24 * 60 * 60)
            
            return TokenResponse(
                access_token=access_token,
            )
            
    
    async def refresh_access_token(self,refresh_token:str|None,response:Response)->TokenResponse:
            if not refresh_token:
                    raise InvalidCredentialsError()
            
            payload = decode_refresh_token(token=refresh_token)
            async with self.uow as uow:
                user = await uow.user_repo.get_by_id(user_id=payload)
                if not user:
                    raise UserNotFoundError()
                new_access_token = create_access_token(user_id=payload)
                new_refresh_token = create_refresh_token(user_id=payload)    
                
                response.set_cookie(key="refresh_token",
                                    value=new_refresh_token,
                                    httponly=True,
                                    secure=False,
                                    max_age=7 * 24 * 60 * 60)
                return TokenResponse(access_token=new_access_token)
            
        

            
        
