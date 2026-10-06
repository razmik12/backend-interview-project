from fastapi import status

from app.exceptions.app_exception import AppError


class EmailAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(
            message="Email already exists",
            code="ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__(
            message="Invalid credentials",
            code="INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class UserNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            message="User not found",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )
