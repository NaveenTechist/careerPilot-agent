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
from uuid import UUID
from repositories.application_repository import (ApplicationRepository,)
from fastapi import APIRouter
from fastapi import Depends
from agents.matching_agent import MatchingAgent
from models.db.match_entity import MatchStatus
from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository
from fastapi import BackgroundTasks
from automation.agents.automation_agent import AutomationAgent
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
        application_repository=ApplicationRepository(),
    ) 

def get_automation_agent():

    return AutomationAgent(
        application_repository=ApplicationRepository(),
        resume_repository=ResumeRepository(),
        job_repository=JobRepository(),
        match_repository=MatchRepository(),
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
        print(result)
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
    background_tasks: BackgroundTasks,
):

    repository = MatchRepository()
    match = repository.update_status(
        match_id,
        MatchStatus.PROCEEDED,
    )

    # Sync corresponding application status
    from database.database import SessionLocal
    from models.db.application_entity import ApplicationEntity, ApplicationStatus
    db = SessionLocal()
    application_id = None
    try:
        app_entity = (
            db.query(ApplicationEntity)
            .filter(ApplicationEntity.match_id == match_id)
            .first()
        )

        if app_entity:
            app_entity.status = ApplicationStatus.PROCEEDED
            application_id = str(app_entity.id)
            db.commit()
    finally:
        db.close()
    if application_id:
        automation_agent = get_automation_agent()

        background_tasks.add_task(
            automation_agent.process,
            application_id,
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

    # Sync corresponding application status
    from database.database import SessionLocal
    from models.db.application_entity import ApplicationEntity, ApplicationStatus
    db = SessionLocal()
    application_id = None
    try:
        app_entity = (
            db.query(ApplicationEntity)
            .filter(ApplicationEntity.match_id == match_id)
            .first()
        )

        if app_entity:
            app_entity.status = ApplicationStatus.CANCELLED
            application_id = str(app_entity.id)
            db.commit()
    finally:
        db.close()
    

    return {

        "message": "Application cancelled.",
        "status": match.status,

    }
@router.get("/current")
def current_match(
    agent: MatchingAgent = Depends(
        get_matching_agent
    ),
):
    result = agent.get_current_match()
    if result is None:
        return {
            "exists": False,
        }
    return {
        "exists": True,
        "match": result,
    }