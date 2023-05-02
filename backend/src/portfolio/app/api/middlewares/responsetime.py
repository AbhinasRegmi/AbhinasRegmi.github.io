import time

from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseTime(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response