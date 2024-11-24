from enum import Enum, auto

class ErrorSeverity(Enum):
    NONE_OPERATIONAL = auto()  # Application can continue operating normally
    LOW_ = auto()  # Application can continue operating normally
    MEDIUM_LIMITED = auto()  # Application can continue operating but with some limitations
    HIGH_MAJOR_ISSUE = auto()  # Application cannot continue to operate without major issues
    CRITICAL_SHUTDOWN = auto()  # Application must shut down or restart
