from models.job_profile import JobProfile
from core.exceptions import JobParsingError

from services.base_llm_parser_service import (
    BaseLLMParserService,
)

from services.job_normalizer import (
    JobNormalizer,
)


class JobParserService(BaseLLMParserService):
    PROMPT_FILE = "job_parser.md"
    MODEL = JobProfile
    NORMALIZER = JobNormalizer
    PARSING_EXCEPTION = JobParsingError
