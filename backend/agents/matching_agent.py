"""
Matching Agent.

Coordinates the resume and
job matching workflow.
"""

from models.match_result import MatchResult

from services.session_service import session
from services.matching_parser_service import (
    MatchingParserService,
)

from core.logger import app_logger
from core.exceptions import MatchingError


class MatchingAgent:

    def __init__(
        self,
        parser: MatchingParserService,
    ):

        self.parser = parser

    def process(
        self,
    ) -> MatchResult:

        app_logger.info(
            "Matching process started."
        )

        if session.session.resume is None:
            raise MatchingError(
                "Resume not uploaded."
            )

        if session.session.job is None:
            raise MatchingError(
                "Job not analyzed."
            )

        prompt = f"""
        Resume Profile
        {session.session.resume.model_dump_json(indent=2)}
        Job Profile
        {session.session.job.model_dump_json(indent=2)}
        """

        result = self.parser.parse(
            prompt
        )

        app_logger.success(
            "Matching completed."
        )

        return result