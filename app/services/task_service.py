import logging
from uuid import UUID

from app.core.uow import UnitOfWork
from app.exceptions.project_exception import (
    NotProjectMemberError,
    ProjectNotFoundError,
)
from app.exceptions.task_exception import (
    NotAllowedError,
    TaskNotFoundError,
)
from app.models.task import TaskORM
from app.schemas.task import TaskCreate, TaskFilter, TaskStatusUpdate, TaskUpdate

from .permissions import require_member, require_owner

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_task(
        self,
        data: TaskCreate,
        project_id: UUID,
        actor_id: UUID,
    ):
        logger.info("Task creation started")
        async with self.uow as uow:
            await require_member(
                uow=uow,
                project_id=project_id,
                user_id=actor_id,
            )

            if data.assigned_id is not None:
                member = await uow.member_repo.get_member(
                    project_id=project_id,
                    user_id=data.assigned_id,
                )

                if not member:
                    logger.warning(
                        "Task creation failed: assignee is not a project member"
                    )
                    raise NotProjectMemberError()

            task = await uow.task_repo.create(
                project_id=project_id,
                assigned_id=data.assigned_id,
                title=data.title,
                description=data.description,
            )

            logger.info("Task created successfully")
            return task

    async def list_tasks(
        self, project_id: UUID, actor_id: UUID, filters: TaskFilter
    ) -> list[TaskORM]:
        logger.debug("Retrieving project tasks")
        async with self.uow as uow:
            await require_member(uow=uow, user_id=actor_id, project_id=project_id)

            tasks = await uow.task_repo.list_by_project(
                project_id=project_id,
                status=filters.status,
                assigned_id=filters.assigned_id,
                limit=filters.limit,
                offset=filters.offset,
            )

            logger.debug("Project tasks retrieved successfully")
            return tasks

    async def update_task(
        self, data: TaskUpdate, project_id: UUID, actor_id: UUID, task_id: UUID
    ) -> TaskORM:
        logger.info("Task update started")
        async with self.uow as uow:
            await require_owner(uow=uow, project_id=project_id, user_id=actor_id)
            task = await uow.task_repo.get_by_id(task_id=task_id)

            if not task or task.project_id != project_id:
                logger.warning("Task update failed: task not found in project")
                raise TaskNotFoundError()

            if data.assigned_id is not None:
                member = await uow.member_repo.get_member(
                    project_id=project_id, user_id=data.assigned_id
                )

                if not member:
                    logger.warning(
                        "Task update failed: assignee is not a project member"
                    )
                    raise NotProjectMemberError()

            updated_task = await uow.task_repo.update(
                task=task, data=data.model_dump(exclude_unset=True)
            )

            logger.info("Task updated successfully")
            return updated_task

    async def update_status(
        self, data: TaskStatusUpdate, actor_id: UUID, task_id: UUID, project_id: UUID
    ) -> TaskORM:
        logger.info("Task status update started")
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)

            if not task:
                logger.warning("Task status update failed: task not found")
                raise TaskNotFoundError()

            project = await uow.project_repo.get_by_id(project_id=project_id)

            if not project:
                logger.warning("Task status update failed: project not found")
                raise ProjectNotFoundError()

            if project.id != task.project_id:
                logger.warning(
                    "Task status update failed: task does not belong to project"
                )
                raise ProjectNotFoundError()

            if actor_id != project.owner_id and actor_id != task.assigned_id:
                logger.warning("Task status update denied: user is not allowed")
                raise NotAllowedError()

            task.status = data.status
            await uow.flush()
            await uow.refresh(task)

            logger.info("Task status updated successfully")
            return task

    async def delete_task(
        self, task_id: UUID, actor_id: UUID, project_id: UUID
    ) -> None:
        logger.info("Task deletion started")
        async with self.uow as uow:
            await require_owner(uow, project_id, actor_id)

            task = await uow.task_repo.get_by_id(task_id=task_id)

            if not task or task.project_id != project_id:
                logger.warning("Task deletion failed: task not found in project")
                raise TaskNotFoundError()

            await uow.task_repo.delete(task=task)
            logger.info("Task deleted successfully")
