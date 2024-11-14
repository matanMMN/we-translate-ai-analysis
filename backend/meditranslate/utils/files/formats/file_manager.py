from abc import ABC, abstractmethod
from io import BytesIO

class FileManager:
    def extract_text(self, file_stream: BytesIO) -> str:
        """Extracts text content from a file."""
        raise NotImplementedError

    def create_file(self, text: str) -> BytesIO:
        raise NotImplementedError
