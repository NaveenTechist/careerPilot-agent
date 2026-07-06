"""
Matching Agent.

Coordinates the resume and
job matching workflow.
"""

from models.match_result import MatchResult
from services.matching_parser_service import (
    MatchingParserService,
)
import json
from core.logger import app_logger
from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository
from repositories.match_repository import MatchRepository
from core.exceptions import MatchingError


class MatchingAgent:
    def __init__(
        self,
        resume_repository: ResumeRepository,
        job_repository: JobRepository,
        match_repository: MatchRepository,
        parser: MatchingParserService,
    ):

        self.resume_repository = resume_repository
        self.job_repository = job_repository
        self.match_repository = match_repository
        self.parser = parser

    def process(
        self,
    ) -> MatchResult:
        app_logger.info("Matching process started.")
        resume = self.resume_repository.get_latest()

        if resume is None:
            raise MatchingError("Resume not found.")
        job = self.job_repository.get_latest()

        if job is None:
            raise MatchingError("Job not found.")
        prompt = f"""
        Resume Profile
        {json.dumps(resume.resume_json, indent=2)}
        Job Profile
        {json.dumps(job.job_json, indent=2)}
        """
        # print("="*80)
        # print("PROMPT:")
        # print(prompt)
        # print("="*80)
        result = self.parser.parse(prompt)

        self.match_repository.save(
            resume_id=resume.id,
            job_id=job.id,
            result=result,
        )

        app_logger.success("Matching completed.")
        return result
