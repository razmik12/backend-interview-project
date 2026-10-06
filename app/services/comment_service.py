from sqlalchemy import UUID

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
            member = await uow.member_repo.get_member(
                project_id=task.project_id, user_id=actor_id
            )
            if not member:
                raise UserNotProjectMemberError()
            return await uow.comment_repo.create(
                task_id=task.id, author_id=actor_id, text=data.text
            )

    async def list_comments(self, actor_id: UUID, task_id: UUID) -> list[CommentORM]:
        async with self.uow as uow:
            task = await uow.task_repo.get_by_id(task_id=task_id)
            if not task:
                raise TaskNotFoundError()
            member = await uow.member_repo.get_member(
                project_id=task.project_id, user_id=actor_id
            )
            if not member:
                raise UserNotProjectMemberError()
            return await uow.comment_repo.list_by_task(task_id=task.id)

    async def delete_comment(self, actor_id: UUID, comment_id: UUID) -> None:
        async with self.uow as uow:
            comment = await uow.comment_repo.get_by_id(comment_id=comment_id)
            if not comment:
                raise CommentNotFoundError()
            task = await uow.task_repo.get_by_id(task_id=comment.task_id)
            if not task:
                raise TaskNotFoundError()
            project = await uow.project_repo.get_by_id(project_id=task.project_id)

            if not project:
                raise ProjectNotFoundError()

            if actor_id != comment.author_id and actor_id != project.owner_id:
                raise NotAllowedError()

            await uow.comment_repo.delete(comment=comment)
