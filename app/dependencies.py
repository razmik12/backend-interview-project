from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from fastapi import Depends
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM
from app.services.auth_service import AuthService
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.config import settings
from app.exceptions.user_exception import UserNotFoundError
from app.repositories.user_repo import UserRepository
from app.services.comment_service import CommentService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

security = HTTPBearer()

async def get_uow_factory(db:AsyncSession = Depends(get_db))->UnitOfWork:
    return  UnitOfWork(session=db)


async def get_auth_service(uow:UnitOfWork = Depends(get_uow_factory))->AuthService:
    return AuthService(uow=uow)


async def get_project_services(uow:UnitOfWork = Depends(get_uow_factory))->ProjectService:
    return ProjectService(uow=uow)



async def get_task_service(uow:UnitOfWork = Depends(get_uow_factory))->TaskService:
    return TaskService(uow=uow)


async def get_comment_service(uow:UnitOfWork = Depends(get_uow_factory))->CommentService:
    return CommentService(uow=uow)


async def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security),db:AsyncSession = Depends(get_db))->UserORM:
    token = credentials.credentials
    repo = UserRepository(session=db)
    user_id = decode_access_token(token)
    user = await repo.get_by_id(user_id=user_id)
    if not user:
        raise UserNotFoundError()
    return user

        
        
        