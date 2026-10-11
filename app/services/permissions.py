import logging
from uuid import UUID

from app.core.uow import UnitOfWork
from app.exceptions.project_exception import (
    NotProjectMemberError,
    NotProjectOwnerError,
    ProjectNotFoundError,
)
from app.models.projectmember import ProjectMemberORM, ProjectMemberRole

logger = logging.getLogger(__name__)


async def require_member(
    uow: UnitOfWork, user_id: UUID, project_id: UUID
) -> ProjectMemberORM:
    if not await uow.project_repo.get_by_id(project_id=project_id):
        logger.warning("Access check failed: project not found")
        raise ProjectNotFoundError()

    member = await uow.member_repo.get_member(project_id=project_id, user_id=user_id)

    if not member:
        logger.warning("Access denied: user is not a project member")
        raise NotProjectMemberError()

    logger.debug("Project membership verified")
    return member


async def require_owner(
    uow: UnitOfWork,
    project_id: UUID,
    user_id: UUID,
) -> ProjectMemberORM:
    member = await require_member(
        uow=uow,
        project_id=project_id,
        user_id=user_id,
    )

    if member.role != ProjectMemberRole.OWNER:
        logger.warning("Access denied: user is not the project owner")
        raise NotProjectOwnerError()

    return member
