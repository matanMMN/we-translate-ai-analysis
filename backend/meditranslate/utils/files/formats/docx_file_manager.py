import tempfile
from meditranslate.utils.files.formats.file_manager import FileManager
from io import BytesIO
from docx import Document


class DocxFileManager(FileManager):
    def extract_text(self, file_stream: BytesIO) -> str:
        # Create a temporary file to store the .docx content
        with tempfile.NamedTemporaryFile(delete=True, mode='wb') as temp_file:
            temp_file.write(file_stream.read())  # Write the BytesIO stream to the temp file
            temp_file_path = temp_file.name  # Get the temporary file path

        # Extract text from the .docx file using python-docx
        doc = Document(temp_file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])

        return text
