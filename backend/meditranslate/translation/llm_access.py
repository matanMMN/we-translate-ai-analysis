from http import HTTPStatus
from typing import List, Dict, Any, Tuple, Optional

from anthropic import AsyncAnthropic, APIStatusError

from meditranslate.app.configurations import config
from meditranslate.app.errors import AppError, ErrorSeverity, ErrorType
from meditranslate.app.loggers import logger


class AnthropicClient:
    def __init__(
            self,
            api_key: str = config.ANTHROPIC_API_KEY,
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

        self.client = AsyncAnthropic(api_key=self.api_key)

    async def translation(self, system_prompt: str, file_contents: str, **params: Any) -> Tuple[str, bool]:
        """
        Sends a message to a Claude LLM, and then repeatedly asks for responses until the LLM responds with either:
            - "end_turn" -          The LLM has reached the end of its response.
            - "stop_sequences" -    The LLM has generated a sequence which was specified as a stopping point.

        The repetition aspect was implememted to overcome Anthropic API's limitation on response size - The API allows
        for a response of up to 4096 tokens, which is not enough for full file translation. Therefore, we request a
        response multiple times, with the old generated response preceeding the current response, to continue
        the translation generation process.

        Returns the output, and a boolean specifying whether the expected tokens appeared and were stripped from the
        output.
        """
        # Set up parameters for call:
        sent_params = dict(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        sent_params.update(params)

        # Send first message:
        response = await self._send_message(
            system_prompt=system_prompt,
            built_message_seq=[{"role": "user", "content": file_contents}],
            **sent_params)

        reps = 1
        output_text = self._parse_response(response)
        stop_reason = response.stop_reason

        # Repeat message sending process until "end_turn" or "stop_sequences" is reached:
        while stop_reason not in ["end_turn", "stop_sequences"] and reps < self.max_reps:
            response = await self._send_message(
                system_prompt=system_prompt,
                built_message_seq=[
                    {"role": "user", "content": file_contents},
                    {"role": "assistant", "content": output_text}
                ],
                **sent_params)

            reps += 1
            output_text += self._parse_response(response)
            stop_reason = response.stop_reason

        # Finalize the translation and return:
        result  = self._finalize_translation(output_text)
        success = True

        # Verify that "end_turn" or "stop_sequences" was indeed reached.
        if stop_reason not in ["end_turn", "stop_sequences"]:
            logger.warning(f"Anthropic could not finish generation before max_reps={self.max_reps} - {stop_reason=}")
            logger.warning(f"Generated output: '''\n{output_text}\n'''")
            success = False

        if result is None:
            result = output_text
            success = False

        return result, success

    async def _send_message(self, system_prompt: str, built_message_seq: List[Dict[str, Any]], **params: Any):
        try:
            response = await self.client.messages.create(
                system=system_prompt,
                messages=built_message_seq,
                **params)

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

            for msg in built_message_seq:
                logger.error(f"{msg}")

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

        for token in [stop_token] + wrap_tokens:
            if token not in translation:
                logger.warning(f"Missing token from LLM output: {token}.")
                missing_token = True

        if missing_token:
            return None

        translation = translation[:translation.index(stop_token)]
        translation = translation[
                      translation.index(wrap_tokens[0]) + len(wrap_tokens[0]):
                      translation.index(wrap_tokens[1])]

        return translation

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def __del__(self):
        self.close()

