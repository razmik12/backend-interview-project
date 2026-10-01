from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.projectmember import ProjectMemberORM
from uuid import UUID



class ProjectMemberRepository:
    def __init__(self,session: AsyncSession):
        self.session = session
    
    async def create_member(self,project_id: UUID , user_id: UUID , role: str ) -> ProjectMemberORM:
        member = ProjectMemberORM(project_id = project_id , user_id = user_id , role = role)
        self.session.add(member)
        await self.session.flush()
        return member
        
    
    async def get_member(self,project_id: UUID,user_id: UUID)-> ProjectMemberORM | None:
        result = await self.session.execute(
        select(ProjectMemberORM)
        .where(
            ProjectMemberORM.project_id == project_id,
            ProjectMemberORM.user_id == user_id,
        )
    )

        return result.scalar_one_or_none()