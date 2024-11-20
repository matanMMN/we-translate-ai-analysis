from meditranslate.app.configurations import config
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType

from meditranslate.translation.text_processor import TextProcessor
from meditranslate.translation.translation_input import FileTranslationInput, TextTranslationInput
from meditranslate.translation.translation_output import FileTranslationOutput, TextTranslationOutput
from meditranslate.translation.prompt_loader import get_sysprompt_construct
from meditranslate.translation.llm_access import AnthropicClient

class TranslationEngine:
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.sysprompt_con = get_sysprompt_construct(version=2)
        self.text_processor = TextProcessor()

    async def translate_file(self, translation_input: FileTranslationInput) -> FileTranslationOutput:
        try:
            src = await self.text_processor.preprocess_src_file(translation_input.input_bytes)
            ref = await self.text_processor.preprocess_ref_file(translation_input.reference_bytes)

            system_prompt = self.sysprompt_con(ref_text=ref)
            translation = await self.anthropic_client.translation(
                system_prompt=system_prompt,
                file_contents=src)

            dst = await self.text_processor.postprocess_result(translation)
            translation_output = FileTranslationOutput(
                output_bytes=dst,
                translation_metadata={
                    "service":"none"
                })

            return translation_output
        except AppError as ae:  # Already handled.
            raise ae
        except Exception as e:
            raise AppError(
                error=e,
                error_class=AppError,
                title="Unexpected Error in Translation Engine",
                description="Some unexpected error has occured in translation engine during file translation.",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )

    async def translate_text(self, translation_input: TextTranslationInput) -> TextTranslationOutput:
        try:
            ref = await self.text_processor.preprocess_ref_file(translation_input.reference_bytes)

            system_prompt = self.sysprompt_con(ref_text=ref)
            translation = await self.anthropic_client.translation(
                system_prompt=system_prompt,
                file_contents=translation_input.input_text)

            translation_output = TextTranslationOutput(
                output_text=translation,
                translation_metadata={
                    "service": "none"
                })
            return translation_output
        except AppError as ae:  # Already handled.
            raise ae
        except Exception as e:
            raise AppError(
                error=e,
                error_class=AppError,
                title="Unexpected Error in Translation Engine",
                description="Some unexpected error has occured in translation engine during text translation.",
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR)
