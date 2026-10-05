import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        print(f"Process Time: {process_time}")
        print(f"Request: {request.method} {request.url} - Status Code: {response.status_code}")
        return response