from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request,Response
from meditranslate.app.loggers import logger
from meditranslate.app.errors.error_handler import ErrorHandler


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            return await ErrorHandler.handle_error(request,e)

