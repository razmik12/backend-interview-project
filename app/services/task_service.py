from uuid import UUID

from app.core.uow import UnitOfWork
from app.exceptions.project_exception import (
    NotProjectMemberError,
    NotProjectOwnerError,
    ProjectNotFoundError,
)
from app.exceptions.task_exception import (
    NotAllowedError,
    TaskNotFoundError,
    UserNotProjectMemberError,
)
from app.models.projectmember import ProjectMemberRole
from app.models.task import TaskORM
from app.schemas.task import TaskCreate, TaskFilter, TaskStatusUpdate, TaskUpdate


class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_task(self, data: TaskCreate, project_id: UUID, actor_id: UUID):
        async with self.uow as uow:
            if not await uow.project_repo.get_by_id(project_id=project_id):
                raise ProjectNotFoundError()

            if not await uow.member_repo.get_member(
                project_id=project_id, user_id=actor_id
            ):
                raise NotProjectMemberError()

            if data.assigned_id is not None:
                assignee_member = await uow.member_repo.get_member(
                    project_id=project_id, user_id=data.assigned_id
                )
                if not assignee_member:
                    raise UserNotProjectMemberError()

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
            projects = await uow.project_repo.get_by_id(project_id=project_id)
            if not projects:
                raise ProjectNotFoundError()
            member = await uow.member_repo.get_member(
                project_id=project_id, user_id=actor_id
            )
            if not member:
                raise NotProjectMemberError()
            tasks = await uow.task_repo.list_by_project(
                project_id=project_id,
                status=filters.status,
                assigned_id=filters.assigned_id,
                limit=filters.limit,
                offset=filters.offset,
            )
            return tasks

    async def update_task(
        self, data: TaskUpdate, project_id: UUID, actor_id: UUID, task_id: UUID
    ) -> TaskORM:
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task:
                raise TaskNotFoundError()
            
            if task.project_id != project_id:
                raise TaskNotFoundError()
            member = await uow.member_repo.get_member(
                project_id=project_id, user_id=actor_id
            )
            if not member:
                raise UserNotProjectMemberError()
            if member.role != ProjectMemberRole.OWNER:
                raise NotProjectOwnerError()
            
            updated_task = await uow.task_repo.update(
                task=task, data=data.model_dump(exclude_unset=True)
            )
            return updated_task

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

    async def delete_task(self, task_id: UUID, owner_id: UUID) -> None:
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task:
                raise TaskNotFoundError()
            project = await uow.project_repo.get_by_id(project_id=task.project_id)
            print("PROJECT:", project)
            if not project:
                raise ProjectNotFoundError()
            if project.owner_id != owner_id:
                raise NotAllowedError()
            await uow.task_repo.delete(task=task)
            return
