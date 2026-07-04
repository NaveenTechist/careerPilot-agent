"""
Job API.
Responsible only for HTTP request handling.

Responsibilities:
- Validate request
- Delegate to JobAgent
- Return structured response

Never:
- Scrape HTML
- Call Gemini
- Parse jobs
"""

import time
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from agents.job_agent import JobAgent
from services.job_scraper_service import JobScraperService
from services.job_parser_service import JobParserService
from core.logger import app_logger
from services.session_service import session
from repositories.job_repository import JobRepository


router = APIRouter(
    prefix="/job",
    tags=["Job"],
)


class JobRequest(BaseModel):
    url: HttpUrl


def get_job_agent() -> JobAgent:
    scraper = JobScraperService()
    parser = JobParserService()
    job_repository = JobRepository
    return JobAgent(
        scraper=scraper,
        parser=parser,
        job_repository=job_repository,
    )


@router.post("/")
def analyze_job(
    request: JobRequest,
    job_agent: JobAgent = Depends(get_job_agent),
):

    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    logger = app_logger.bind(request_id=request_id)

    logger.info("Job analysis request received.")

    try:
        profile = job_agent.process(str(request.url))
        job_repository.save(profile)
        logger.success(
            "Job saved to session."
        )
        return profile

    except Exception:
        logger.exception("Job analysis failed.")
        raise
    finally:
        elapsed = (time.perf_counter() - start) * 1000

        logger.info(f"Request completed in {elapsed:.2f} ms")
