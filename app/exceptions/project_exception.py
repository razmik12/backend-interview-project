from app.exceptions.app_exception import AppError
from fastapi import status


class ProjectNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            message="Project not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )

class NotProjectMemberError(AppError):
    def __init__(self):
        super().__init__(
            message="You are not a member of this project",
            code="NOT_PROJECT_MEMBER",
            status_code=status.HTTP_403_FORBIDDEN,
        )

class NotProjectOwnerError(AppError):
    def __init__(self):
        super().__init__(
            message="You are not the owner of this project",
            code="NOT_PROJECT_OWNER",
            status_code=status.HTTP_403_FORBIDDEN,
        )
        


class UserAlreadyMemberError(AppError):
    def __init__(self):
        super().__init__(
            message="User already exists in project",
            code="ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT,)
        
        

    