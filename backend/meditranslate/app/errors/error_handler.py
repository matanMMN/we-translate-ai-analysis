import traceback
from .app_error import AppError, ErrorSeverity, ErrorType, HTTPStatus
from fastapi import Request
from meditranslate.app.loggers import logger
from fastapi import Response
from fastapi.responses import JSONResponse

from http import  HTTPStatus
from pydantic import ValidationError
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import  IntegrityError
from meditranslate.app.shared.schemas import BaseResponseSchema

def is_subclass_of_exception(exc_instance):
    return isinstance(exc_instance, Exception) and type(exc_instance) is not Exception


class ErrorHandler:
    @staticmethod
    async def handle_error(request: Request, app_error: Exception) -> Response:
        logger.error("ERROR IN ERROR HANDLER")
        status_code, error_response = ErrorHandler._get_error_response(app_error)
        ErrorHandler._log_error(request, app_error, status_code)
        response = BaseResponseSchema(
            error=str(error_response['error']),
            status_code=status_code,
        )
        return JSONResponse(
            content=response.model_dump(),
            status_code=status_code,
            headers=ErrorHandler._get_default_headers(),
        )

    @staticmethod
    def _get_error_response(app_error: Exception) -> tuple:

        if isinstance(app_error, AppError):
            return app_error.http_status.value if app_error.http_status else HTTPStatus.INTERNAL_SERVER_ERROR.value, {"error": app_error.get_user_message()}

        elif isinstance(app_error, HTTPException):
            return app_error.status_code, {"error": app_error.detail}

        elif isinstance(app_error,StarletteHTTPException):
            return HTTPStatus.BAD_REQUEST.value, {"error": "Validation Error", "details": str(app_error)}

        elif isinstance(app_error,RequestValidationError):
            return HTTPStatus.BAD_REQUEST.value, {"error": "Validation Error", "details": str(app_error)}

        elif isinstance(app_error, ValidationError):
            return HTTPStatus.BAD_REQUEST.value, {"error": "Validation Error", "details": str(app_error)}

        elif isinstance(app_error,IntegrityError): # custom parsing is needed for this.
            return HTTPStatus.CONFLICT.value, {"error": f"Database Integrity Error"}

        elif isinstance(app_error, SQLAlchemyError):
            return HTTPStatus.INTERNAL_SERVER_ERROR.value, {"error": "Database error occurred. Please try again later."}

        elif isinstance(app_error, AttributeError):
            return HTTPStatus.BAD_REQUEST.value, {"error": "An attribute error occurred. Please check your input."}

        elif isinstance(app_error, ValueError):
            return HTTPStatus.BAD_REQUEST.value, {"error": "A value error occurred. Please check your input."}

        elif isinstance(app_error, TypeError):
            return HTTPStatus.BAD_REQUEST.value, {"error": "A type error occurred. Please check your input."}

        elif isinstance(app_error, Exception):
            if is_subclass_of_exception(app_error):
                logger.critical(f"exception class was not catched: {type(app_error)}")
            return HTTPStatus.INTERNAL_SERVER_ERROR.value, {"error": "An unexpected error occurred."}

        else:
            return HTTPStatus.INTERNAL_SERVER_ERROR.value, {"error": "An unexpected error occurred."}

    @staticmethod
    def _log_error(request: Request, app_error: Exception, status_code: int):
        logger.error(
            f"""
                URL: {str(request.url)}
                Status Code: {status_code}
                Exception: {type(app_error).__name__}
                Message: {str(app_error)}
                Traceback: {traceback.format_exc()}
            """
        )

    @staticmethod
    def _get_default_headers() -> dict:
        return {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "no-referrer",
        }
