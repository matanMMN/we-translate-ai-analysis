
from enum import Enum


class FileSizeUnit(str, Enum):
    BYTES = "Bytes"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"
