from http import HTTPStatus
from io import BytesIO
from typing import Dict, Optional

from meditranslate.app.errors import AppError, ErrorSeverity, ErrorType
from meditranslate.utils.files.temporary_file_handler import TemporaryFileHandler


class LocalFilesContext:
    def __init__(self, bytes_map: Dict[str, Optional[BytesIO]]):
        self._temp_file_handler = TemporaryFileHandler("/tmp/files/translation_engine/")
        self._bytes_map: Optional[Dict[str, BytesIO]] = bytes_map

        # Temporary local file paths:
        self._path_map: Optional[Dict[str, str]] = None

    def __enter__(self):
        self._path_map = {}

        for name, bytes_ in self._bytes_map.items():
            if bytes_ is None:
                bytes_ = BytesIO()

            self._path_map[name] = self._temp_file_handler.save_file(bytes_, name, "translator")

        self._bytes_map = None
        return self

    def get_path(self, file_name: str):
        if self._path_map is None:
            raise AppError(
                title="Developer Error: Error in LocalFilesContext",
                description="Temporary source file was not created (Use LocalFilesContext in a `with` statement).",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )

        if file_name not in self._path_map.keys():
            raise AppError(
                title="Developer Error: Error in LocalFilesContext",
                description=f"No temporary source file with name={file_name}.",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )

        return self._path_map[file_name]


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._temp_file_handler.delete_temp_directory()

        self._path_map = None
