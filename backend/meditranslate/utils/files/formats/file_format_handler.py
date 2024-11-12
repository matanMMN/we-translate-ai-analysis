from io import BytesIO
from meditranslate.utils.files.file_format_type import FileFormatType
from meditranslate.utils.files.formats.doc_file_manager import DocFileManager
from meditranslate.utils.files.formats.docx_file_manager import DocxFileManager
from meditranslate.utils.files.formats.file_manager import FileManager
from meditranslate.utils.files.formats.html_file_manager import HtmlFileManager
from meditranslate.utils.files.formats.pdf_file_manager import PdfFileManager
from meditranslate.utils.files.formats.txt_file_manager import TxtFileManager

class FileFormatHandler:
    def __init__(self):
        self._handlers = {
            FileFormatType.TXT: TxtFileManager(),
            FileFormatType.PDF: PdfFileManager(),
            FileFormatType.DOCX: DocxFileManager(),
            FileFormatType.DOC: DocFileManager(),
            FileFormatType.HTML: HtmlFileManager()
        }

    def get_handler(self, file_format: FileFormatType) -> FileManager:
        """Return the appropriate handler based on file format type."""
        handler =  self._handlers.get(file_format,None)
        if not handler:
            raise ValueError(f"Unsupported file format: {file_format}")
        return handler

    def extract_text(self, file_format: FileFormatType, file_stream: BytesIO) -> str:
        """Extract text from the file."""
        handler = self.get_handler(file_format)
        return handler.extract_text(file_stream)

    def create_file(self, file_format: FileFormatType, text: str) -> BytesIO:
        handler = self.get_handler(file_format)
        file_io = handler.create_file(text)
        file_io.seek(0)
        return file_io


    def get_content_type(self,file_format:FileFormatType) -> str:
        handler = self.get_handler(file_format)
        return handler.get_content_type()

