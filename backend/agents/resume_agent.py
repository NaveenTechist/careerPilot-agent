"""
Resume Agent

Coordinates the resume extraction workflow.

Responsibilities
----------------
1. Validate resume
2. Call PDF Service
3. Return structured response
"""

from pathlib import Path

from services.pdf_service import PDFService
from models.resume import ResumeResponse
from core.logger import app_logger
from core.exceptions import InvalidResumeError
from services.resume_parser_service import ResumeParserService
from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository


class ResumeAgent:
    def __init__(
        self,
        pdf_service: PDFService,
        parser_service: ResumeParserService,
        resume_repository: ResumeRepository,
        job_repository: JobRepository,
    ):

        self.pdf_service = pdf_service
        self.parser_service = parser_service
        self.resume_repository = resume_repository
        self.job_repository = job_repository

    def process_resume(self, pdf_path: Path) -> ResumeResponse:

        app_logger.info("Resume processing started.")

        if pdf_path.suffix.lower() != ".pdf":
            raise InvalidResumeError("Only PDF resumes are supported.")

        text, pages = self.pdf_service.extract_text(pdf_path)

        profile = self.parser_service.parse(text)

        # Copy the PDF to permanent storage
        import shutil
        import uuid
        permanent_dir = Path("storage/resumes")
        permanent_dir.mkdir(parents=True, exist_ok=True)
        permanent_path = permanent_dir / f"{uuid.uuid4()}.pdf"
        shutil.copy2(pdf_path, permanent_path)

        entity = self.resume_repository.save(profile=profile, pdf_path=str(permanent_path))

        app_logger.success("Resume processed successfully. 🔥🔥🔥")

        return entity
