from sqlalchemy import UUID

from app.models.project import ProjectORM
from app.schemas.projects import ProjectCreate,ProjectOut
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
            