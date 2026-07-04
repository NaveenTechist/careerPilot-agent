from models.match_result import MatchResult

from services.base_llm_parser_service import (
    BaseLLMParserService,
)

from services.matching_normalizer import (
    MatchingNormalizer,
)

class MatchingParserService(
    BaseLLMParserService,
):

    PROMPT_FILE = "matching.md"
    MODEL = MatchResult
    NORMALIZER = MatchingNormalizer()