from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import TaskORM


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        project_id: UUID,
        assigned_id: UUID,
        title: str,
        description: str | None = None,
    ) -> TaskORM:
        task = TaskORM(
            project_id=project_id,
            assigned_id=assigned_id,
            title=title,
            description=description,
        )
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_by_id(self, task_id) -> TaskORM | None:
        return await self.session.get(TaskORM, task_id)

    async def list_by_project(
        self,
        project_id: UUID,
        status: str | None,
        assigned_id: UUID | None,
        limit: int,
        offset: int,
    ) -> list[TaskORM]:
        query = select(TaskORM).where(TaskORM.project_id == project_id)

        if status is not None:
            query = query.where(TaskORM.status == status)
        if assigned_id is not None:
            query = query.where(TaskORM.assigned_id == assigned_id)

        query = (
            query.order_by(
                TaskORM.created_at,
                TaskORM.id,
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, task: TaskORM, data: dict) -> TaskORM:
        for key, value in data.items():
            setattr(task, key, value)

        await self.session.flush()
        await self.session.refresh(task)

        return task

    async def delete(self, task: TaskORM) -> None:
        await self.session.delete(task)
