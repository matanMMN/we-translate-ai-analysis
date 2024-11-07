from enum import Enum


class FileFormatType(str, Enum):
    TXT = "txt"
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    GIF = "gif"

class FileFormatType(str,Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    HTML = "html"
    MD = "md"
    TXT = "txt"
