from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import ProjectORM
from uuid import UUID



class ProjectRepository:
    def __init__(self,session: AsyncSession):
        self.session = session
    
    async def create_project(self,name: str,owner_id: UUID,description: str | None = None) -> ProjectORM:
        project = ProjectORM(name = name, description = description, owner_id = owner_id)
        self.session.add(project)
        await self.session.flush()
        return project
    
    async def get_by_id(self,project_id: UUID) -> ProjectORM | None:
        return await self.session.get(ProjectORM , project_id)
    
    
    
    