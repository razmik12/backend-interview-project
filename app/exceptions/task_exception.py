from app.exceptions.app_exception import AppError
from fastapi import status


class TaskNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            message="Task not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,)
        
        
class UserNotProjectMemberError(AppError):
    def __init__(self):
            super().__init__(
                message="Member not found",
                code="NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,)





class NotAllowedError(AppError):
    def __init__(self):
            super().__init__(
                message="Not allowed",
                code="NOT_ALLOWED",
                status_code=status.HTTP_403_FORBIDDEN,)