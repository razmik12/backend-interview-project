import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from .app_exception import AppError

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if exc.status_code >= 500:
        logger.error(
            "Application error: code=%s, status_code=%s, path=%s",
            exc.code,
            exc.status_code,
            request.url.path,
        )

    elif exc.status_code >= 400:
        logger.info(
            "Application request rejected: code=%s, status_code=%s, path=%s",
            exc.code,
            exc.status_code,
            request.url.path,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )
