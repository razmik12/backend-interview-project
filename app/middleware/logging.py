import logging
from time import perf_counter

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

logger = logging.getLogger("app.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            process_time_ms = (perf_counter() - start_time) * 1000

            logger.exception(
                "Request failed | Method: %s | Path: %s | "
                "Status Code: 500 | Duration: %.2f ms",
                request.method,
                request.url.path,
                process_time_ms,
            )
            raise

        process_time_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "Request completed | Method: %s | Path: %s | "
            "Status Code: %s | Duration: %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            process_time_ms,
        )

        return response
