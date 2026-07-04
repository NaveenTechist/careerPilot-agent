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


class ResumeAgent:
    def __init__(self, pdf_service=PDFService, parser_service=ResumeParserService):

        self.pdf_service = pdf_service
        self.parser_service = parser_service

    def process_resume(self, pdf_path: Path) -> ResumeResponse:

        app_logger.info("Resume processing started.")

        if pdf_path.suffix.lower() != ".pdf":
            raise InvalidResumeError("Only PDF resumes are supported.")

        text, pages = self.pdf_service.extract_text(pdf_path)

        profile = self.parser_service.parse(text)

        app_logger.success("Resume processed successfully. 🔥🔥🔥")

        return profile
