from io import BytesIO
import pypandoc

from meditranslate.utils.files.temporary_file_handler import TemporaryFileHandler
from meditranslate.app.errors.app_error import AppError, HTTPStatus, ErrorType, ErrorSeverity


class LocalFilesContext:
    def __init__(
            self,
            src_bytes: BytesIO, src_fname: str,
            ref_bytes: BytesIO, ref_fname: str,
            user_id: str):
        self.temp_file_handler = TemporaryFileHandler("/tmp/files/translate/")
        self.src_bytes = src_bytes
        self.src_fname = src_fname
        self.ref_bytes = ref_bytes
        self.ref_fname = ref_fname
        self.user_id = user_id

        # Temporary local file paths:
        self._src_fpath = self._ref_fpath = None

    @property
    def src_fpath(self):
        if self._src_fpath is None:
            raise AppError(
                title="Dev Error: Error in file context",
                description="Temporary source file was not created (Use LocalFilesContext in a `with` statement).",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )

        return self._src_fpath

    @property
    def ref_fpath(self):
        if self._ref_fpath is None:
            raise AppError(
                title="Dev Error: Error in file context",
                description="Temporary source file was not created (Use LocalFilesContext in a `with` statement).",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )

        return self._ref_fpath

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def docx_stream_to_html(file: BytesIO) -> str:
        pass

