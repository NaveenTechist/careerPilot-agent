"""
Resume API.

Responsible only for HTTP requests.

It should NEVER:
- Extract PDF
- Call Gemini
- Compare skills

Its responsibility is request handling.
"""

from pathlib import Path
import uuid
import time

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from starlette import status
from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository
from agents.resume_agent import ResumeAgent
from services.pdf_service import PDFService
from core.config import settings
from core.logger import app_logger
from services.resume_parser_service import (
    ResumeParserService,
)
from services.session_service import session

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


def get_resume_agent():
    pdf_service = PDFService()
    parser_service = ResumeParserService()
    repository = ResumeRepository()
    job_repository = JobRepository()
    return ResumeAgent(
        pdf_service=pdf_service,
        parser_service=parser_service,
        resume_repository=repository,
        job_repository=job_repository

    )


@router.post("/")
async def upload_resume(
    file: UploadFile = File(...),
    resume_agent: ResumeAgent = Depends(get_resume_agent),
):
    """
    Upload a resume PDF.
    """
    start = time.perf_counter()

    request_id = str(uuid.uuid4())

    logger = app_logger.bind(
        request_id=request_id,
        filename=file.filename,
    )

    logger.info("Resume upload request received")

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    unique_name = f"{uuid.uuid4()}.pdf"

    temp_path = Path(settings.TEMP_DIRECTORY) / unique_name

    try:
        content = await file.read()

        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeded.",
            )

        temp_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with temp_path.open("wb") as buffer:
            buffer.write(content)

        result = resume_agent.process_resume(
            temp_path
        )

        logger.success(
            "Resume saved to session."
        )
        return result

    except Exception:
        logger.exception("Resume processing failed.")

        raise

    finally:
        elapsed = time.perf_counter() - start

        logger.info("Resume request completed")

        if temp_path.exists():
            temp_path.unlink()

        await file.close()
