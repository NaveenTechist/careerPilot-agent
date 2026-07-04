"""
PDF Service

Responsible only for reading PDF files.

It should NEVER know anything about:
- APIs
- FastAPI
- AI
- Resume Matching

Single Responsibility Principle.
"""

from pathlib import Path
import fitz

from core.logger import app_logger
from core.exceptions import ResumeExtractionError


class PDFService:
    """
    Handles all PDF operations.
    """

    def extract_text(self, pdf_path: Path) -> tuple[str, int]:
        """
        Extract text from a PDF.
        Returns
        -------
        tuple
            (text, page_count)
        """

        app_logger.info(f"Opening PDF: {pdf_path.name}")

        try:
            document = fitz.open(pdf_path)
            text = ""
            for page in document:
                text += page.get_text()
            pages = len(document)
            document.close()
            app_logger.success(f"Successfully extracted {pages} pages.")
            return text, pages

        except Exception as e:
            app_logger.exception("PDF extraction failed.")
            raise ResumeExtractionError("Unable to extract text from resume.") from e
