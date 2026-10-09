from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import CommentORM


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task_id: UUID, author_id: UUID, text: str) -> CommentORM:
        comment = CommentORM(task_id=task_id, author_id=author_id, text=text)
        self.session.add(comment)
        await self.session.flush()
        return comment

    async def get_by_id(self, comment_id: UUID) -> CommentORM | None:
        return await self.session.get(CommentORM, comment_id)

    async def list_by_task(self, task_id: UUID) -> list[CommentORM]:
        result = await self.session.execute(select(CommentORM)
        .where(CommentORM.task_id == task_id).order_by(
            CommentORM.created_at,
            CommentORM.id,
                ))
        return result.scalars().all()

    async def delete(self, comment: CommentORM) -> None:
        await self.session.delete(comment)
