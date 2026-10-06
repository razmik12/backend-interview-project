from fastapi import status

from app.exceptions.app_exception import AppError


class CommentNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            message="Comment not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
