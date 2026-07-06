"""
Matching API.
Responsible only for HTTP.
Never
- Match skills
- Call Gemini
- Save database directly
"""

import time
import uuid
from fastapi import APIRouter
from fastapi import Depends
from agents.matching_agent import MatchingAgent
from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository
from repositories.match_repository import MatchRepository
from services.matching_parser_service import (
    MatchingParserService,
)

from core.logger import app_logger

router = APIRouter(
    prefix="/match",
    tags=["Matching"],
)

# ------------------------------------------------------


def get_matching_agent():
    return MatchingAgent(
        resume_repository=ResumeRepository(),
        job_repository=JobRepository(),
        match_repository=MatchRepository(),
        parser=MatchingParserService(),
    )


# ------------------------------------------------------


@router.post("/")
def analyze(
    agent: MatchingAgent = Depends(get_matching_agent),
):
    request_id = str(uuid.uuid4())
    logger = app_logger.bind(
        request_id=request_id,
    )
    start = time.perf_counter()
    logger.info("Matching request received.")
    try:
        result = agent.process()
        logger.success("Matching completed.")
        return result
    except Exception:
        logger.exception("Matching failed.")
        raise
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(f"Completed in {elapsed:.2f} ms")

@router.post("/{match_id}/proceed")
def proceed_match(
    match_id: UUID,
):

    repository = MatchRepository()

    match = repository.update_status(
        match_id,
        MatchStatus.PROCEEDED,
    )

    return {

        "message": "Application approved.",

        "status": match.status,

    }

@router.post("/{match_id}/cancel")
def cancel_match(
    match_id: UUID,
):

    repository = MatchRepository()

    match = repository.update_status(
        match_id,
        MatchStatus.CANCELLED,
    )

    return {

        "message": "Application cancelled.",

        "status": match.status,

    }