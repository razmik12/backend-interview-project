from sqlalchemy import UUID

from app.models.project import ProjectORM
from app.schemas.projects import ProjectCreate,ProjectOut,ProjectDetailOut
from app.exceptions.project_exception import ProjectNotFoundError,NotProjectMemberError,NotProjectOwnerError
from app.core.uow import UnitOfWork
from app.models.projectmember import ProjectMemberRole

class ProjectService:
    def __init__(self,uow: UnitOfWork):
        self.uow = uow

    async def create_project(self,data:ProjectCreate,owner_id:UUID)->ProjectORM:
        async with self.uow as uow:
            project = await uow.project_repo.create_project(name = data.name ,owner_id = owner_id , description = data.description)
            await uow.member_repo.create_member(project_id = project.id, user_id = owner_id, role = ProjectMemberRole.OWNER)
            return project

    async def list_my_projects(self,user_id:UUID)->list[ProjectOut]:
        async with self.uow as uow:
            projects = await  uow.project_repo.get_projects(user_id=user_id)
            return projects
        
    async def get_project_detail(self,project_id:UUID,user_id:UUID) -> ProjectORM:
        async with self.uow as uow:
            project = await uow.project_repo.get_with_members(project_id=project_id)
            if not project:
                raise ProjectNotFoundError()
            member = await uow.member_repo.get_member(project_id=project.id,user_id=user_id)
            if not member:
                raise NotProjectMemberError()
            
            return project
        