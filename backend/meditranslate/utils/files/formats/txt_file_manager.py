from meditranslate.utils.files.formats.file_manager import FileManager
from io import BytesIO


class TxtFileManager(FileManager):
    def extract_text(self, file_stream: BytesIO) -> str:
        file_content = file_stream.read()
        return file_content

    def create_file(self, text: str) -> BytesIO:
        file_content = text.encode('utf-8')
        file_stream = BytesIO(file_content)
        return file_stream
