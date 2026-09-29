from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project_member_repo import ProjectMemberRepository
from app.repositories.project_repo import ProjectRepository
from app.repositories.user_repo import UserRepository
from app.database import async_session

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.user_repo = UserRepository(session=self.session)
        self.project_repo = ProjectRepository(session=self.session)
        self.member_repo = ProjectMemberRepository(session=self.session)
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()
    
    async def commit(self):
         await self.session.commit()
        
    async def rollback(self):
         await self.session.rollback()
        
    async def flush(self):
         await self.session.flush()
        
        