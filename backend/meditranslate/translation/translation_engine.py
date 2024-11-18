from meditranslate.translation.text_processor import TextProcessor
from meditranslate.translation.translation_input import TranslationInput
from meditranslate.translation.translation_output import TranslationOutput
from meditranslate.app.configurations import config
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType


class TranslationEngine:
    async def translate_file(self, translation_input: TranslationInput) -> TranslationOutput:
        try:
            text_processor = TextProcessor()

            src, ref = await text_processor.preprocess_files(
                translation_input.input_bytes, translation_input.reference_bytes)

            dst = await text_processor.postprocess_result(src)

            translation_output = TranslationOutput(
                output_bytes=dst,
                translation_metadata={
                    "service":"none"
                }
            )
            return translation_output
        except Exception as e:
            raise AppError(
                error=e,
                error_class=AppError,
                title="error in translation engine",
                description="",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )
