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
from repositories.application_repository import (
    ApplicationRepository,
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
        application_repository: ApplicationRepository,
        parser: MatchingParserService,
    ):
        self.resume_repository = resume_repository
        self.job_repository = job_repository
        self.match_repository = match_repository
        self.parser = parser
        self.application_repository = application_repository

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

        application_name = f"{job.company} - {job.job_title}"

        application = self.application_repository.save(
            resume_id=resume.id,
            job_id=job.id,
            match_id=entity.id,
            title=application_name,
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

    def get_current_match(self):
        """
        Get latest match without regenerating.
        """
        app_logger.info(
            "Checking existing match."
        )
        resume = self.resume_repository.get_latest()

        if resume is None:
            return None

        job = self.job_repository.get_latest()

        if job is None:
            return None

        # OOPS
        entity = self.match_repository.get_latest_by_resume_job(
            resume.id,
            job.id,
        )

        if entity is None:
            return None

        return {
            "match_id": str(entity.id),
            "status": entity.status.value,
            **entity.match_json,
        }