from meditranslate.utils.files.formats.file_manager import FileManager
from io import BytesIO


class HtmlFileManager(FileManager):
    def extract_text(self, file_stream: BytesIO) -> str:
        raise NotImplementedError
