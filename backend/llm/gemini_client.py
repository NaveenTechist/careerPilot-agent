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
from google.genai.errors import APIError, ClientError, ServerError

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

from core.config import settings
from core.exceptions import LLMServiceError
from core.logger import app_logger


def _is_transient_gemini_error(exc: Exception) -> bool:
    """
    Determine if an exception from Gemini is transient and should be retried.
    Transient errors include:
    - Any ServerError (HTTP 5xx status codes).
    - APIError/ClientError representing rate limits (HTTP 429 status code).
    """
    if isinstance(exc, ServerError):
        return True
    if isinstance(exc, APIError):
        return exc.code == 429
    return False


def _before_sleep_log(retry_state) -> None:
    """
    Log warnings before sleeping between retry attempts for transient errors.
    """
    exc = retry_state.outcome.exception()
    attempt = retry_state.attempt_number
    sleep_time = retry_state.upcoming_sleep

    if isinstance(exc, APIError) and exc.code == 429:
        app_logger.warning(
            f"Gemini API rate limit hit (Attempt {attempt}/3). Retrying in {sleep_time:.2f}s..."
        )
    elif isinstance(exc, ServerError):
        app_logger.warning(
            f"Gemini server error {exc.code} (Attempt {attempt}/3). Retrying in {sleep_time:.2f}s..."
        )
    else:
        app_logger.warning(
            f"Gemini call failed with transient error (Attempt {attempt}/3). Retrying in {sleep_time:.2f}s... Error: {exc}"
        )


class GeminiClient:
    """
    Wrapper around Google's Gemini API.
    """

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )
        self.model = settings.MODEL_NAME

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
        try:
            return self._generate(prompt)

        except ClientError as exc:
            if exc.code == 429:
                app_logger.exception("Gemini API rate limit exceeded.")
                raise LLMServiceError(
                    "Gemini rate limit exceeded. Please try again in a few moments."
                ) from exc

            app_logger.exception("Gemini client error occurred.")
            raise LLMServiceError(
                f"Invalid request to Gemini: {exc.message}"
            ) from exc

        except ServerError as exc:
            app_logger.exception("Gemini unavailable after retries.")
            raise LLMServiceError(
                "Gemini temporarily unavailable. Please try again in a few moments."
            ) from exc

        except APIError as exc:
            app_logger.exception("Gemini API error occurred.")
            raise LLMServiceError(
                f"Gemini API returned an error: {exc.message}"
            ) from exc

        except LLMServiceError:
            # Re-raise already wrapped LLMServiceErrors
            raise

        except Exception as exc:
            app_logger.exception("Unexpected Gemini error.")
            raise LLMServiceError(
                "Failed to communicate with Gemini."
            ) from exc

    @retry(
        retry=retry_if_exception(_is_transient_gemini_error),
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=2,
            min=2,
            max=10,
        ),
        before_sleep=_before_sleep_log,
        reraise=True,
    )
    def _generate(
        self,
        prompt: str,
    ) -> str:
        app_logger.info("Sending request to Gemini.")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise LLMServiceError(
                "Gemini returned an empty response."
            )

        app_logger.success("Gemini response received.")
        return response.text
