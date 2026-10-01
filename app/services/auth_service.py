from app.models.user import UserORM
from app.schemas.user import UserCreate,UserLogin,TokenResponse
from app.exceptions.user_exception import EmailAlreadyExistsError,InvalidCredentialsError
from app.core.security import verify_password,hash_password
from app.core.uow import UnitOfWork
from sqlalchemy.exc import IntegrityError
from app.core.security import create_access_token,create_refresh_token

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
           
    async def login(self,data:UserLogin)->TokenResponse:
        async with self.uow as uow:
            user = await uow.user_repo.get_by_email(email=data.email)
            if not user:
                raise InvalidCredentialsError()
            if not verify_password(password=data.password,hashed_password=user.hashed_password):
                raise InvalidCredentialsError()
            
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            
        
