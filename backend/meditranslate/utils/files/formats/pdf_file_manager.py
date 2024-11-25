import tempfile
from meditranslate.utils.files.formats.file_manager import FileManager
from io import BytesIO
import pdfplumber

class PdfFileManager(FileManager):
    def extract_text(self, file_stream: BytesIO) -> str:
        with tempfile.NamedTemporaryFile(delete=True, mode='wb') as temp_file:
            temp_file.write(file_stream.read())  # Write the BytesIO stream to the temp file
            temp_file_path = temp_file.name  # Get the temporary file path

        text = []
        with pdfplumber.open(temp_file_path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text())
                
        return "\n".join(text)
