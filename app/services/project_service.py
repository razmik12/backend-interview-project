import logging
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.core.uow import UnitOfWork
from app.exceptions.project_exception import (
    NotProjectOwnerError,
    ProjectNotFoundError,
    UserAlreadyMemberError,
)
from app.exceptions.user_exception import UserNotFoundError
from app.models.project import ProjectORM
from app.models.projectmember import ProjectMemberORM, ProjectMemberRole
from app.schemas.projects import MemberAdd, ProjectCreate, ProjectUpdate

from .permissions import require_member

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_project(self, data: ProjectCreate, owner_id: UUID) -> ProjectORM:
        logger.info("Project creation started")
        async with self.uow as uow:
            project = await uow.project_repo.create_project(
                name=data.name, owner_id=owner_id, description=data.description
            )
            await uow.member_repo.create_member(
                project_id=project.id, user_id=owner_id, role=ProjectMemberRole.OWNER
            )

            logger.info("Project created successfully")
            return project

    async def list_my_projects(self, user_id: UUID) -> list[ProjectORM]:
        logger.debug("Retrieving user's projects")
        async with self.uow as uow:
            projects = await uow.project_repo.get_projects(user_id=user_id)

            logger.debug("User projects retrieved successfully")
            return projects

    async def get_project_detail(self, project_id: UUID, user_id: UUID) -> ProjectORM:
        logger.debug("Retrieving project details")
        async with self.uow as uow:
            await require_member(
                uow,
                project_id=project_id,
                user_id=user_id,
            )

            project = await uow.project_repo.get_with_members(project_id=project_id)
            if not project:
                logger.warning("Project details failed: project not found")
                raise ProjectNotFoundError()

            logger.debug("Project details retrieved successfully")
            return project

    async def update_project(
        self, project_id: UUID, user_id: UUID, data: ProjectUpdate
    ) -> ProjectORM:
        logger.info("Project update started")
        async with self.uow as uow:
            project = await uow.project_repo.get_by_id(project_id=project_id)

            if not project:
                logger.warning("Project update failed: project not found")
                raise ProjectNotFoundError()

            if project.owner_id != user_id:
                logger.warning("Project update denied: user is not the owner")
                raise NotProjectOwnerError()

            upd_data = data.model_dump(exclude_unset=True)

            updated_project = await uow.project_repo.update_project(
                project=project, data=upd_data
            )

            logger.info("Project updated successfully")
            return updated_project

    async def delete_project(self, user_id: UUID, project_id: UUID) -> None:
        logger.info("Project deletion started")
        async with self.uow as uow:
            project = await uow.project_repo.get_by_id(project_id=project_id)

            if not project:
                logger.warning("Project deletion failed: project not found")
                raise ProjectNotFoundError()

            elif project.owner_id != user_id:
                logger.warning("Project deletion denied: user is not the owner")
                raise NotProjectOwnerError()

            await uow.project_repo.delete_project(project=project)
            logger.info("Project deleted successfully")

    async def add_member(
        self, project_id: UUID, data: MemberAdd, owner_id: UUID
    ) -> ProjectMemberORM:
        logger.info("Adding project member started")
        async with self.uow as uow:
            project = await uow.project_repo.get_by_id(project_id=project_id)

            if not project:
                logger.warning("Adding project member failed: project not found")
                raise ProjectNotFoundError()

            if project.owner_id != owner_id:
                logger.warning("Adding project member denied: user is not the owner")
                raise NotProjectOwnerError()

            user = await uow.user_repo.get_by_id(user_id=data.user_id)

            if not user:
                logger.warning("Adding project member failed: user not found")
                raise UserNotFoundError()

            existing_member = await uow.member_repo.get_member(
                project_id=project.id, user_id=user.id
            )
            if existing_member:
                logger.warning("Adding project member failed: user is already a member")
                raise UserAlreadyMemberError()

            try:
                member = await uow.member_repo.create_member(
                    project_id=project.id,
                    user_id=data.user_id,
                    role=ProjectMemberRole.MEMBER,
                )
            except IntegrityError:
                logger.warning(
                    "Adding project member failed: database integrity constraint violation"
                )
                raise UserAlreadyMemberError()

            logger.info("Project member added successfully")
            return member
