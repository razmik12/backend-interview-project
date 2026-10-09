import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        end_time = f"Process Time: {process_time}"

        logger.info(
            "Time: %s | Request: %s %s | Status Code: %s",
            end_time,
            request.method,
            request.url,
            response.status_code,
        )

        return response
