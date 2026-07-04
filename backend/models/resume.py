"""
Pydantic models for Resume APIs.
"""

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    success: bool
    filename: str
    pages: int
    characters: int
    text: str
