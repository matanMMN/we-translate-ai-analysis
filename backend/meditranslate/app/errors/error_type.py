from enum import Enum, auto
from typing import Any, Optional, Dict, List, Union

class ErrorType(Enum):
    HTTP_ERROR = "HTTP Error"
    VALIDATION_ERROR = "Validation Error"
    DATABASE_ERROR = "Database Error"
    AUTHENTICATION_ERROR = "Authentication Error"
    AUTHORIZATION_ERROR = "Authorization Error"
    NOT_FOUND_ERROR = "Not Found Error"
    CONFLICT_ERROR = "Conflict Error"
    SERVER_ERROR = "Server Error"
    CLIENT_ERROR = "Client Error"
    CUSTOM_ERROR = "Custom Error"
    NETWORK_ERROR = "Network Error"
    RESOURCE_LIMIT_ERROR = "Resource Limit Error"
    TIMEOUT_ERROR = "Timeout Error"
    EXTERNAL_SERVICE_ERROR = "external service Error"

