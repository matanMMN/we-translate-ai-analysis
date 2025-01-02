from http import HTTPStatus
from typing import List, Dict, Any, Tuple, Optional
import google.generativeai as genai

from anthropic import AsyncAnthropic, APIStatusError
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
from meditranslate.app.configurations import config
from meditranslate.app.errors import AppError, ErrorSeverity, ErrorType
from meditranslate.app.loggers import logger


class GeminiClient:
    def __init__(
            self,
            api_key: str = config.GOOGLE_API_KEY,
            model_name: str = config.ANTHROPIC_MODEL_NAME,
            max_tokens: int = config.CLAUDE_MAX_TOKENS,
            temperature: float = config.CLAUDE_TEMPERATURE,
            max_reps: int = config.CLAUDE_MAX_REPS
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_reps = max_reps
        genai.configure(api_key=self.api_key)

    async def translation(self, system_prompt: str, file_contents: str, **params: Any) -> Tuple[str, bool]:

        response = await self._send_message(system_prompt, file_contents, **params)
        text = response.text
        result  = self._finalize_translation(text)
        success = True
        print("RESULT: ", result, success)
        return result, success

    async def _send_message(self, system_prompt: str, file_contents: str, **params: Any):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
            response = model.generate_content(
                file_contents,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=4096,
                    temperature=0.2)
            )

            return response

        except APIStatusError as e:
            raise AppError(
                error=e,
                error_class=AppError,
                title="Error from Anthropic API",
                description=f"Some error has occured when utilizing Anthropic API: {e.message}",
                http_status=HTTPStatus(e.status_code),
                context="translation engine",
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                operable=False,
                error_type=ErrorType.TRANSLATION_ERROR,
            )
        except Exception as e:
            logger.error(f"Some error has occurred when sending a message to the underlying client.")
            logger.error(f"System Prompt=\n{system_prompt}")
            logger.error(f"Message Sequence=[")
            logger.error(f"Added Params={params}")
            logger.error(f"\nRaised: {e}")

            raise AppError(
                error=e,
                error_class=AppError,
                title="Developer Error: Send Message to Anthropic",
                description="Error occured while sending a message to an Anthropic client",
                operable=False,
                severity=ErrorSeverity.HIGH_MAJOR_ISSUE,
                error_type=ErrorType.TRANSLATION_ERROR,
                http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                user_message="Something went wrong during file translation.")

    @staticmethod
    def _parse_response(response: Any) -> str:
        return response.content[0].text.rstrip()

    @staticmethod
    def _finalize_translation(translation: str) -> Optional[str]:
        """
        Attempts to finalize the translation by stripping stop and wrapping tokens. If any token was not found, returns
        `None` to indicate a token was missing.
        """
        stop_token = "[TRANSLATION_SUCCESSFUL]"
        wrap_tokens = ["<eng_text>", "</eng_text>"]
        missing_token = False
        
        # for token in [stop_token] + wrap_tokens:
        #     if token not in translation:
        #         logger.warning(f"Missing token from LLM output: {token}.")
        #         missing_token = True

        # if missing_token:
        #     return None


        cleaned_html_string = translation.replace("[TRANSLATION_SUCCESSFUL]", "")

        # translation = translation[:translation.index(stop_token)]
        # translation = translation[
        #               translation.index(wrap_tokens[0]) + len(wrap_tokens[0]):
        #               translation.index(wrap_tokens[1])]
        print("TRANSLATION: ", cleaned_html_string)
        return cleaned_html_string

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def __del__(self):
        self.close()

