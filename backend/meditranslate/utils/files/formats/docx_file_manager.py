from meditranslate.utils.files.formats.file_manager import FileManager
from io import BytesIO


class DocxFileManager(FileManager):
    def extract_text(self, file_stream: BytesIO) -> str:
        raise NotImplementedError
