from fastapi import status

from app.exceptions.app_exception import AppError


class TaskNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            message="Task not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UserNotProjectMemberError(AppError):
    def __init__(self):
        super().__init__(
            message="User is not a member of this project",
            code="NOT_PROJECT_MEMBER",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class NotAllowedError(AppError):
    def __init__(self):
        super().__init__(
            message="Not allowed",
            code="NOT_ALLOWED",
            status_code=status.HTTP_403_FORBIDDEN,
        )
