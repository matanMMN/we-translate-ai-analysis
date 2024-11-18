from typing import Optional, Dict, Tuple
from io import BytesIO

import pypandoc
import docx

from meditranslate.utils.files.temporary_file_handler import TemporaryFileHandler
from meditranslate.app.errors.app_error import AppError, HTTPStatus, ErrorType, ErrorSeverity
from meditranslate.app.loggers import logger


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


class TextProcessor:
    @staticmethod
    def _docx_to_html(fpath: str):
        return pypandoc.convert_file(fpath, to="html")

    @staticmethod
    def _html_to_docx(content: str, fpath: str):
        return pypandoc.convert_text(content, format="html", to="docx", outputfile=fpath)

    @staticmethod
    def _docx_to_text(fpath: str):
        doc = docx.Document(fpath)
        full_text = []

        for para in doc.paragraphs:
            full_text.append(para.text)

        return '\n'.join(full_text)

    async def preprocess_files(self, src_bytes: BytesIO, ref_bytes: BytesIO) -> Tuple[str, str]:
        with LocalFilesContext({"src.docx": src_bytes, "ref.docx": ref_bytes}) as lf_con:
            src_html = self._docx_to_html(lf_con.get_path("src.docx"))
            ref_text = self._docx_to_text(lf_con.get_path("ref.docx"))

        return src_html, ref_text

    async def postprocess_result(self, result: str) -> BytesIO:
        with LocalFilesContext({"dst.docx": None}) as lf_con:
            self._html_to_docx(result, lf_con.get_path("dst.docx"))

            with open(lf_con.get_path("dst.docx"), "rb") as result_file:
                result_bytes = BytesIO(result_file.read())
                result_bytes.seek(0)

        return result_bytes