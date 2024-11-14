from enum import Enum


class FileContentType(Enum):
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"
    HTML = "text/html"
    MD = "text/markdown"
    TXT = "text/plain"
    PNG = "image/png"
    JPG = "image/jpeg"
    JPEG = "image/jpeg"
    GIF = "image/gif"
