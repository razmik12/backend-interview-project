from fastapi import Request
from fastapi.responses import JSONResponse

from .app_exception import AppError


async def app_exception_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )
