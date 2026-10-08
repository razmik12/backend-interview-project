from uuid import UUID
from sqlalchemy.exc import IntegrityError

from app.core.uow import UnitOfWork
from app.exceptions.project_exception import (
    NotProjectMemberError,
    NotProjectOwnerError,
    ProjectNotFoundError,
    UserAlreadyMemberError,
)
from app.exceptions.user_exception import UserNotFoundError
from app.models.project import ProjectORM
from app.models.projectmember import ProjectMemberORM, ProjectMemberRole
from app.schemas.projects import MemberAdd, ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_project(self, data: ProjectCreate, owner_id: UUID) -> ProjectORM:
        async with self.uow as uow:
            project = await uow.project_repo.create_project(
                name=data.name, owner_id=owner_id, description=data.description
            )
            await uow.member_repo.create_member(
                project_id=project.id, user_id=owner_id, role=ProjectMemberRole.OWNER
            )
            return project

    async def list_my_projects(self, user_id: UUID) -> list[ProjectORM]:
        async with self.uow as uow:
            projects = await uow.project_repo.get_projects(user_id=user_id)
            return projects

    async def get_project_detail(self, project_id: UUID, user_id: UUID) -> ProjectORM:
        async with self.uow as uow:
            project = await uow.project_repo.get_with_members(project_id=project_id)
            if not project:
                raise ProjectNotFoundError()
            member = await uow.member_repo.get_member(
                project_id=project.id, user_id=user_id
            )
            if not member:
                raise NotProjectMemberError()

            return project

    async def update_project(
        self, project_id, user_id, data: ProjectUpdate
    ) -> ProjectORM:
        async with self.uow as uow:
            project = await uow.project_repo.get_by_id(project_id=project_id)
            if not project:
                raise ProjectNotFoundError()
            if project.owner_id != user_id:
                raise NotProjectOwnerError()
            upd_data = data.model_dump(exclude_unset=True)
            return await uow.project_repo.update_project(project=project, data=upd_data)

    async def delete_project(self, user_id: UUID, project_id: UUID) -> None:
        async with self.uow as uow:
            project = await uow.project_repo.get_by_id(project_id=project_id)
            if not project:
                raise ProjectNotFoundError()
            elif project.owner_id != user_id:
                raise NotProjectOwnerError()
            await uow.project_repo.delete_project(project=project)

    async def add_member(
        self, project_id: UUID, data: MemberAdd, owner_id: UUID
    ) -> ProjectMemberORM:
        async with self.uow as uow:
            project = await uow.project_repo.get_by_id(project_id=project_id)
            if not project:
                raise ProjectNotFoundError()
            elif project.owner_id != owner_id:
                raise NotProjectOwnerError()
            user = await uow.user_repo.get_by_id(user_id=data.user_id)
            if not user:
                raise UserNotFoundError()

            existing_member = await uow.member_repo.get_member(
                project_id=project.id, user_id=user.id
            )
            if existing_member:
                raise UserAlreadyMemberError()
            try:
                member = await uow.member_repo.create_member(
                    project_id=project.id,
                    user_id=data.user_id,
                    role=ProjectMemberRole.MEMBER,            
                )
            except IntegrityError:
                    raise UserAlreadyMemberError()
            return member
