from io import BytesIO

import pypandoc
import docx

from meditranslate.translation.text_processing.local_file_context import LocalFilesContext
from meditranslate.translation.text_processing.html_processing import HTMLProcessor


class TextProcessor:
    def __init__(self):
        self.html_processor = HTMLProcessor()

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

    async def preprocess_src_file(self, src_bytes: BytesIO) -> str:
        with LocalFilesContext({"src.docx": src_bytes}) as lf_con:
            src_html = self._docx_to_html(lf_con.get_path("src.docx"))

        return src_html

    async def preprocess_ref_file(self, ref_bytes: BytesIO) -> str:
        with LocalFilesContext({"ref.docx": ref_bytes}) as lf_con:
            ref_text = self._docx_to_text(lf_con.get_path("ref.docx"))

        return ref_text

    async def postprocess_result(self, result: str) -> BytesIO:
        with LocalFilesContext({"dst.docx": None}) as lf_con:
            processed_result = self.html_processor.process(result)

            self._html_to_docx(processed_result, lf_con.get_path("dst.docx"))

            with open(lf_con.get_path("dst.docx"), "rb") as result_file:
                result_bytes = BytesIO(result_file.read())
                result_bytes.seek(0)

        return result_bytes