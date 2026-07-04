"""
Job Profile Models.

Represents a structured job description.
"""

from typing import List

from pydantic import BaseModel, Field


class JobProfile(BaseModel):
    company: str | None = None
    job_title: str
    location: str | None = None
    employment_type: str | None = None
    experience: str | None = None
    education: str | None = None
    salary: str | None = None

    application_url: str | None = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
