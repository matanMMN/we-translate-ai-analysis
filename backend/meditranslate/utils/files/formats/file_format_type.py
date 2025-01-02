from enum import Enum


class FileFormatType(str,Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    HTML = "html"
    MD = "md"
    TXT = "txt"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    GIF = "gif"
