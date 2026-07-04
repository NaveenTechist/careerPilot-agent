from pathlib import Path

from services.pdf_service import PDFService
from services.resume_parser_service import ResumeParserService

pdf = PDFService()

text, pages = pdf.extract_text(Path("sample_resume.pdf"))

parser = ResumeParserService()

profile = parser.parse(text)

print(profile.model_dump_json(indent=4))
