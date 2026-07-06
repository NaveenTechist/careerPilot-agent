"""
User Session Model.

Represents the complete
AI workflow state.

Resume
↓

Job

↓

Matching

↓

Application
"""

from enum import Enum

from pydantic import BaseModel

from models.resume_profile import ResumeProfile
from models.job_profile import JobProfile
from models.match_result import MatchResult


class SessionStatus(str, Enum):
    WAITING_FOR_RESUME = "WAITING_FOR_RESUME"

    WAITING_FOR_JOB = "WAITING_FOR_JOB"

    READY_FOR_MATCHING = "READY_FOR_MATCHING"

    MATCH_COMPLETED = "MATCH_COMPLETED"

    APPLICATION_STARTED = "APPLICATION_STARTED"

    APPLICATION_COMPLETED = "APPLICATION_COMPLETED"


class UserSession(BaseModel):
    status: SessionStatus = SessionStatus.WAITING_FOR_RESUME

    resume: ResumeProfile | None = None

    job: JobProfile | None = None

    # Sprint-2
    match: MatchResult | None = None

    # Sprint-4
    browser_session_id: str | None = None
