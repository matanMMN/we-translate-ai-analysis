from typing import Optional, Union, Dict, Any, Tuple, Type
from .error_type import ErrorType
from .error_severity import ErrorSeverity
from http import HTTPStatus
import traceback
import inspect

class AppError(Exception):
    app_name: Optional[str] = None  # Class-level attribute for app context

    def __init__(
        self,
        error: Any = None,
        error_class: Optional[Type[Exception]] = None,  # Type of exception for more granular handling
        title: str = "",
        description: Optional[str] = "",
        context: Optional[str] = "",
        operable: Optional[bool] = True,
        severity: Optional[ErrorSeverity] = ErrorSeverity.NONE_OPERATIONAL,
        error_type: Optional[ErrorType] = ErrorType.HTTP_ERROR,
        http_status: Optional[HTTPStatus] = HTTPStatus.INTERNAL_SERVER_ERROR,  # Default to 500
        user_message: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        *args: Optional[Tuple[Any, ...]],
        **kwargs: Optional[Dict[str, Any]]
    ):
        # Initialize base Exception with error message
        super().__init__(str(error) if error else "An application error occurred")

        # Instance attributes
        self.error = error
        self.error_class = error_class or type(self)  # Default to AppError if no class is provided
        self.title = title
        self.description = description
        self.context = context
        self.operable = operable
        self.severity = severity
        self.error_type = error_type
        self.http_status = http_status
        self.user_message = user_message
        self.headers = headers if headers else {}
        self.args = args
        self.kwargs = kwargs

        # Capture file, line, and function information of the caller using `inspect`
        caller_frame = inspect.stack()[1]  # Frame 1 is the caller of AppError
        self.file_name = caller_frame.filename
        self.line_number = caller_frame.lineno
        self.function_name = caller_frame.function

    @classmethod
    def set_context(cls, app_name: str):
        """Set application name context as a class-level attribute."""
        cls.app_name = app_name

    def get_user_message(self) -> str:
        """Return user message if available, otherwise the HTTP message."""
        return self.user_message if self.user_message else self.http_status.description

    def __str__(self):
        """Return a verbose string representation of the error."""
        error_details = [
            f"App: {self.app_name}" if self.app_name else "App: Not specified",
            f"Error Class: {self.error_class.__name__ if self.error_class else 'Not specified'}",
            f"Title: {self.title}",
            f"Description: {self.description or 'No additional description provided'}",
            f"Context: {self.context or 'General'}",
            f"Operable: {self.operable}",
            f"Severity: {self.severity.name if self.severity else 'Not specified'}",
            f"Error Type: {self.error_type.name if self.error_type else 'Not specified'}",
            f"HTTP Status: {self.http_status.name if self.http_status else 'Not specified'}",
            f"User Message: {self.get_user_message()}",
            f"File: {self.file_name}",
            f"Line: {self.line_number}",
            f"Function: {self.function_name}",
            f"Headers: {self.headers if self.headers else 'No headers'}",
            f"Args: {self.args if self.args else 'No additional args'}",
            f"Kwargs: {self.kwargs if self.kwargs else 'No additional kwargs'}",
        ]
        return "\n".join(error_details)

    def _log_format(self, level: str) -> str:
        """Helper method to format log messages with a severity level."""
        return f"{level}: {self.__str__()}"

    def _info(self):
        """Log informational level error details."""
        return self._log_format("INFO")

    def _debug(self):
        """Log debugging information about the error."""
        debug_info = [
            self._log_format("DEBUG"),
            f"Traceback: {traceback.format_exc()}",
            f"Exception Type: {self.error_class.__name__ if self.error_class else 'Unknown'}",
            f"File: {self.file_name}, Line: {self.line_number}, Function: {self.function_name}"
        ]
        return "\n".join(debug_info)

    def _trace(self):
        """Log traceback for in-depth debugging."""
        trace_info = [
            self._log_format("TRACE"),
            f"Traceback: {traceback.format_exc()}",
            f"Exception Type: {self.error_class.__name__ if self.error_class else 'Unknown'}",
            f"File: {self.file_name}, Line: {self.line_number}, Function: {self.function_name}"
        ]
        return "\n".join(trace_info)

    def _warn(self):
        """Log warning level error."""
        return self._log_format("WARNING")

    def _error(self):
        """Log the error message."""
        return self._log_format("ERROR")

    def _fatal(self):
        """Log fatal error message."""
        return self._log_format("FATAL")
