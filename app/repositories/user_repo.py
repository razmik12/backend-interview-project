from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserORM
from uuid import UUID
from sqlalchemy import select

class UserRepository:
    def  __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self,user_id: UUID) -> UserORM | None:
        return await self.session.get(UserORM,user_id)
    
    async def get_by_email(self,email: str) -> UserORM | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create_user(self,email: str,full_name: str,hashed_password: str) -> UserORM:
        user = UserORM(email = email,full_name = full_name,hashed_password = hashed_password)
        self.session.add(user)
        await self.session.flush()
        return user
        