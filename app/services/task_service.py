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


class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_task(
        self,
        data: TaskCreate,
        project_id: UUID,
        actor_id: UUID,
    ):
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
                    raise NotProjectMemberError()

            return await uow.task_repo.create(
                project_id=project_id,
                assigned_id=data.assigned_id,
                title=data.title,
                description=data.description,
            )

    async def list_tasks(
        self, project_id: UUID, actor_id: UUID, filters: TaskFilter
    ) -> list[TaskORM]:
        async with self.uow as uow:
            await require_member(uow=uow, user_id=actor_id, project_id=project_id)
            return await uow.task_repo.list_by_project(
                project_id=project_id,
                status=filters.status,
                assigned_id=filters.assigned_id,
                limit=filters.limit,
                offset=filters.offset,
            )

    async def update_task(
        self, data: TaskUpdate, project_id: UUID, actor_id: UUID, task_id: UUID
    ) -> TaskORM:
        async with self.uow as uow:
            await require_owner(uow=uow, project_id=project_id, user_id=actor_id)
            task = await uow.task_repo.get_by_id(task_id=task_id)

            if not task or task.project_id != project_id:
                raise TaskNotFoundError()
            if data.assigned_id is not None:
                member = await uow.member_repo.get_member(
                    project_id=project_id, user_id=data.assigned_id
                )
                if not member:
                    raise NotProjectMemberError()

            return await uow.task_repo.update(
                task=task, data=data.model_dump(exclude_unset=True)
            )

    async def update_status(
        self, data: TaskStatusUpdate, actor_id: UUID, task_id: UUID, project_id: UUID
    ) -> TaskORM:
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task:
                raise TaskNotFoundError()
            project = await uow.project_repo.get_by_id(project_id=project_id)
            if not project:
                raise ProjectNotFoundError()
            if project.id != task.project_id:
                raise ProjectNotFoundError()
            if actor_id != project.owner_id and actor_id != task.assigned_id:
                raise NotAllowedError()
            task.status = data.status
            await uow.flush()
            await uow.refresh(task)
            return task

    async def delete_task(
        self, task_id: UUID, actor_id: UUID, project_id: UUID
    ) -> None:
        async with self.uow as uow:
            await require_owner(uow, project_id, actor_id)
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task or task.project_id != project_id:
                raise TaskNotFoundError()
            await uow.task_repo.delete(task=task)
