from uuid import UUID

from app.core.uow import UnitOfWork
from app.exceptions.comment_exception import CommentNotFoundError
from app.exceptions.project_exception import ProjectNotFoundError
from app.exceptions.task_exception import (
    NotAllowedError,
    TaskNotFoundError,
    UserNotProjectMemberError,
)
from app.models.comment import CommentORM
from app.schemas.comment import CommentCreate
from app.services.permissions import require_member,require_owner

class CommentService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create(
        self, task_id: UUID, actor_id: UUID, data: CommentCreate
    ) -> CommentORM:
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task:
                raise TaskNotFoundError()
            await require_member(uow=uow,
                                 user_id=actor_id,
                                 project_id=task.project_id)
            
            return await uow.comment_repo.create(
                task_id=task.id, author_id=actor_id, text=data.text
            )

    async def list_comments(self, actor_id: UUID, task_id: UUID) -> list[CommentORM]:
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task:
                raise TaskNotFoundError()
            await require_member(uow=uow,
                                 user_id=actor_id,
                                 project_id=task.project_id)
            
            return await uow.comment_repo.list_by_task(task_id=task.id)

    async def delete_comment(self, actor_id: UUID, comment_id: UUID) -> None:
        async with self.uow as uow:
            comment = await uow.comment_repo.get_by_id(comment_id=comment_id)
            if not comment:
                raise CommentNotFoundError()
            task = await uow.task_repo.get_by_id(task_id=comment.task_id)
            if not task:
                raise TaskNotFoundError()

            if actor_id != comment.author_id:
                await require_owner(
                    uow=uow,
                    project_id=task.project_id,
                    user_id=actor_id,
                )

            await uow.comment_repo.delete(comment=comment)
