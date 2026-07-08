"""
Matching Agent.

Coordinates the resume and
job matching workflow.
"""

import json

from models.match_result import MatchResult

from services.matching_parser_service import (
    MatchingParserService,
)

from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository
from repositories.match_repository import MatchRepository

from core.logger import app_logger
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

    def process(self):

        app_logger.info(
            "Matching process started."
        )

        # -----------------------------------
        # Get Latest Resume
        # -----------------------------------

        resume = self.resume_repository.get_latest()

        if resume is None:
            raise MatchingError(
                "Resume not found."
            )

        # -----------------------------------
        # Get Latest Job
        # -----------------------------------

        job = self.job_repository.get_latest()

        if job is None:
            raise MatchingError(
                "Job not found."
            )

        # -----------------------------------
        # Check Existing Match
        # -----------------------------------

        existing = self.match_repository.get_by_resume_job(
            resume.id,
            job.id,
        )

        if existing:

            app_logger.info(f"Cached match returned. match_id={existing.id}")

            return {
                "match_id": str(existing.id),
                "status": existing.status.value,
                **existing.match_json,
            }

        # -----------------------------------
        # Build Prompt
        # -----------------------------------

        prompt = f"""
            Resume Profile
            {json.dumps(resume.resume_json, indent=2)}

            Job Profile
            {json.dumps(job.job_json, indent=2)}
        """

        # -----------------------------------
        # Gemini
        # -----------------------------------

        result: MatchResult = self.parser.parse(
            prompt
        )

        # -----------------------------------
        # Save Match
        # -----------------------------------

        entity = self.match_repository.save(
            resume_id=resume.id,
            job_id=job.id,
            result=result,
        )

        app_logger.success(
            f"New match created. id={entity.id}"
        )

        # -----------------------------------
        # Return Response
        # -----------------------------------

        return {
            "match_id": str(entity.id),
            "status": entity.status.value,
            **result.model_dump(),
        }