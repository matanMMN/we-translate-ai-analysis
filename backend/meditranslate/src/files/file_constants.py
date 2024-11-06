from enum import Enum

class FileFormatType(str,Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    HTML = "html"
    MD = "md"
    TXT = "txt"


class FileSizeUnit(str, Enum):
    BYTES = "Bytes"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"

class FileStorageProvider(str,Enum):
    MONGO_GRID_FS = "mongodb_grid_fs"
    LOCAL = "local"
