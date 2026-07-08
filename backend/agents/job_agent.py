"""
Job Agent.

Coordinates the complete
job processing pipeline.
"""

from services.job_scraper_service import (
    JobScraperService,
)
from services.hashing_service import HashingService

from services.job_parser_service import (
    JobParserService,
)

from models.job_profile import JobProfile
from repositories.job_repository import JobRepository

from core.logger import app_logger
from pathlib import Path


class JobAgent:
    def __init__(
        self,
        scraper: JobScraperService,
        parser: JobParserService,
        repository: JobRepository,
    ):
        self.scraper = scraper
        self.parser = parser
        self.repository = repository
    
    def process(
        self,
        url: str,
    ) -> JobProfile:

        app_logger.info(
            "Checking cached job."
        )

        job_hash = HashingService.text_sha256(url)

        existing = self.repository.get_by_hash(
            job_hash
        )

        if existing:
            app_logger.success(
                f"Cached job found. id={existing.id}"
            )
            return existing

        app_logger.info("Job processing started.")
        job_text = self.scraper.scrape(url)

        Path("temp/job_text.txt").write_text(
            job_text,
            encoding="utf-8",
        )

        profile = self.parser.parse(job_text)
        profile.application_url = url
        self.repository.save(profile)
        app_logger.success("Job processing completed.")

        return profile
