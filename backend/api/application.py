"""
Application API.

Provides endpoints for creating, listing, and retrieving job applications.

Responsibilities
----------------
- POST /application - Create complete job application from PDF resume + Job URL.
- GET /applications - List all applications.
- GET /applications/{id} - Retrieve details of a specific application.
"""

from pathlib import Path
import uuid
import time
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from starlette import status

from agents.application_agent import ApplicationAgent
from api.resume import get_resume_agent
from api.job import get_job_agent
from api.matching import get_matching_agent

from repositories.application_repository import ApplicationRepository
from repositories.match_repository import MatchRepository
from database.database import SessionLocal
from models.db.resume_entity import ResumeEntity
from models.db.job_entity import JobEntity

from core.logger import app_logger
from core.config import settings

# Create router without prefix to support both /application and /applications
router = APIRouter(
    tags=["Application"],
)

def get_application_agent():
    return ApplicationAgent(
        resume_agent=get_resume_agent(),
        job_agent=get_job_agent(),
        matching_agent=get_matching_agent(),
    )

# -----------------------------------------------------
# POST /application (with or without trailing slash)
# -----------------------------------------------------

@router.post("/application")
@router.post("/application/")
async def create_application(
    resume: UploadFile = File(...),
    job_url: str = Form(...),
    agent: ApplicationAgent = Depends(get_application_agent),
):
    request_id = str(uuid.uuid4())
    logger = app_logger.bind(
        request_id=request_id,
    )
    start = time.perf_counter()
    logger.info("Application request received.")

    # Validate PDF content type
    if resume.content_type != "application/pdf" and not resume.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resumes are supported.",
        )

    storage = Path("storage/resumes")

    storage.mkdir(
        parents=True,
        exist_ok=True,
    )

    resume_path = storage / f"{uuid.uuid4()}.pdf"
    try:
        resume_path.parent.mkdir(parents=True, exist_ok=True)
        content = await resume.read()

        # Validate file size (10MB limit)
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Resume size exceeds 10MB.",
            )

        resume_path.write_bytes(content)
        result = agent.process(
            resume_path=resume_path,
            job_url=job_url,
        )
        logger.success("Application created.")
        return result
    except Exception as e:
        logger.exception("Failed to create application.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        if temp.exists():
            temp.unlink()
        await resume.close()
        logger.info(
            f"Completed in {(time.perf_counter()-start)*1000:.2f} ms"
        )

# -----------------------------------------------------
# GET /applications (with or without trailing slash)
# -----------------------------------------------------

@router.get("/applications")
@router.get("/applications/")
def list_applications():
    app_repo = ApplicationRepository()
    match_repo = MatchRepository()

    try:
        applications = app_repo.get_all()
        results = []
        for app in applications:
            match = match_repo.get_by_id(app.match_id)
            score = match.score if match else 0
            results.append({
                "id": str(app.id),
                "title": app.title,
                "resume_id": str(app.resume_id),
                "job_id": str(app.job_id),
                "match_id": str(app.match_id),
                "status": app.status.value if hasattr(app.status, "value") else str(app.status),
                "score": score,
                "created_at": app.created_at.isoformat() if app.created_at else None,
                "updated_at": app.updated_at.isoformat() if app.updated_at else None,
            })
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve applications: {str(e)}"
        )

# -----------------------------------------------------
# GET /applications/{id}
# -----------------------------------------------------

@router.get("/applications/{application_id}")
def get_application_details(application_id: UUID):
    app_repo = ApplicationRepository()
    match_repo = MatchRepository()

    app_entity = app_repo.get_by_id(application_id)
    if not app_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found."
        )

    match_entity = match_repo.get_by_id(app_entity.match_id)
    if not match_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matching details not found."
        )

    match_details = match_entity.match_json if match_entity.match_json else {}

    db = SessionLocal()
    try:
        res_db = db.query(ResumeEntity).filter(ResumeEntity.id == app_entity.resume_id).first()
        job_db = db.query(JobEntity).filter(JobEntity.id == app_entity.job_id).first()

        resume_summary = res_db.resume_json.get("summary") if (res_db and res_db.resume_json) else ""
        job_summary = job_db.job_json.get("summary") if (job_db and job_db.job_json) else ""

        if not job_summary and job_db:
            # Fallback if no explicit summary is set in job profile JSON
            company = job_db.company or "Target Company"
            title = job_db.job_title or "Target Job Title"
            job_summary = f"Job listing for a {title} position at {company}."
    finally:
        db.close()

    return {
        "id": str(app_entity.id),
        "title": app_entity.title,
        "resume_id": str(app_entity.resume_id),
        "job_id": str(app_entity.job_id),
        "match_id": str(app_entity.match_id),
        "status": app_entity.status.value if hasattr(app_entity.status, "value") else str(app_entity.status),
        "score": match_entity.score,
        "created_at": app_entity.created_at.isoformat() if app_entity.created_at else None,
        "resume_summary": resume_summary,
        "job_summary": job_summary,
        **match_details,
    }