import logging
import time
from typing import Any, Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware



class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_data = self._request_logging_data(request)
        try:
            now = time.time()
            response = await call_next(request)
            differance = time.time() - now
            request_data.update(
                {
                    "status_code": response.status_code,
                    "time": differance,
                }
            )
            logging.info("Request", extra=request_data)
        except Exception as e:
            request_data.update({"status_code": 500, "time": 0, "error": e})
            logging.exception("Error", exc_info=None, extra=request_data)
            raise e

        return response

    @classmethod
    def _request_logging_data(cls, request: Request) -> dict[str, Any]:
        return {
            "method": request.method,
            "endpoint_url": request.url.path,
            "path_params": request.path_params,
            "query_params": request.query_params,
        }


def build_middlewares() -> list[Middleware]:
    middlewares = []
    origins = [
        "*",
    ]

    middlewares.append(
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"],
        )
    )

    middlewares.append(Middleware(RequestLogMiddleware))
    return middlewares
