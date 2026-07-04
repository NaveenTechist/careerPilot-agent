"""
Gemini Client

Single Responsibility:
- Communicate with Gemini.
- Handle retries.
- Handle transient failures.

It knows nothing about:
- Resume
- Jobs
- Matching
- Browser Automation
"""

from google import genai
from google.genai.errors import ServerError

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from core.config import settings
from core.exceptions import LLMServiceError
from core.logger import app_logger


class GeminiClient:
    """
    Wrapper around Google's Gemini API.
    """

    def __init__(self) -> None:

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.MODEL_NAME

    @retry(
        retry=retry_if_exception_type(ServerError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=2,
            min=2,
            max=10,
        ),
        reraise=True,
    )
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini.

        Returns
        -------
        str
            Raw response text.
        """
        app_logger.info("Sending request to Gemini.")

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            app_logger.success("Gemini response received.")

            if not response.text:
                raise LLMServiceError("Gemini returned an empty response.")

            return response.text

        except ServerError as exc:
            app_logger.exception("Gemini service unavailable.")

            raise LLMServiceError("Gemini API temporarily unavailable.") from exc

        except Exception as exc:
            app_logger.exception("Unexpected Gemini error.")

            raise LLMServiceError("Failed to communicate with Gemini.") from exc
