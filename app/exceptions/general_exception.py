from fastapi import status

from app.exceptions.app_exception import AppError


class LockAcquisitionError(AppError):
    def __init__(self):
        super().__init__(
            message="could not acquire lock",
            code="LOCK_ACQUISITION_ERROR",
            status_code=status.HTTP_409_CONFLICT,
        )


class RateLimitExceededError(AppError):
    def __init__(self):
        super().__init__(
            message="rate limit exceeded",
            code="RARE_LIMITING_ERROR",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )
