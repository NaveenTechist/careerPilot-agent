"""
Resume Profile Models.

These models represent the structured resume
used throughout the application.

Every future agent (Matching, Browser, Job)
will consume this model instead of raw text.
"""

from typing import List
from pydantic import BaseModel, EmailStr, Field


class Education(BaseModel):
    institution: str
    degree: str
    specialization: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    grade: str | None = None


class Experience(BaseModel):
    company: str
    role: str
    start_date: str | None = None
    end_date: str | None = None
    location: str | None = None
    responsibilities: List[str] = Field(default_factory=list)


class Project(BaseModel):
    title: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    github: str | None = None
    live_url: str | None = None


class ResumeProfile(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None
    summary: str | None = None
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
