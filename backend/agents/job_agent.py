"""
Job Agent.

Coordinates the complete
job processing pipeline.
"""

from services.job_scraper_service import (
    JobScraperService,
)

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
        job_repository: JobRepository
    ):
        self.scraper = scraper
        self.parser = parser
        self.job_repository = job_repository

    def process(
        self,
        url: str,
    ) -> JobProfile:
        app_logger.info("Job processing started.")
        job_text = self.scraper.scrape(url)

        Path("temp/job_text.txt").write_text(
            job_text,
            encoding="utf-8",
        )

        profile = self.parser.parse(job_text)
        app_logger.success("Job processing completed.")

        return profile
