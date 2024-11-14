import tempfile
from meditranslate.utils.files.formats.file_manager import FileManager
from io import BytesIO
import pypandoc

class DocFileManager(FileManager):
    def extract_text(self, file_stream: BytesIO) -> str:
        # Create a temporary file to store the file content, automatically deleted after use
        with tempfile.NamedTemporaryFile(delete=True, mode='wb') as temp_file:
            temp_file.write(file_stream.read())  # Write the BytesIO stream to the temp file
            temp_file_path = temp_file.name  # Get the file path of the temporary file
        text = pypandoc.convert_file(temp_file_path, 'plain')  # 'plain' preserves basic text structure
        return text
