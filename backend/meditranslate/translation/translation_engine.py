
from meditranslate.translation.translation_input import TranslationInput
from meditranslate.translation.translation_output import TranslationOutput
from meditranslate.app.configurations import config
from meditranslate.app.errors import AppError,ErrorSeverity,HTTPStatus,ErrorType

class TranslationEngine:

    def __init__(self):
        pass

    async def translate(self,translation_input:TranslationInput) -> TranslationOutput:
        try:
            translation_output = await self._translate()
            return TranslationOutput()
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

    async def _translate(self):
        pass

