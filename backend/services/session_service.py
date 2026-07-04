"""
Session Service.

Temporary in-memory storage.
"""

from models.user_session import (
    UserSession,
    SessionStatus,
)

from models.resume_profile import ResumeProfile
from models.job_profile import JobProfile

from core.logger import app_logger


class SessionService:

    def __init__(self):

        self.session = UserSession()

    # --------------------
    # Resume
    # --------------------

    def save_resume(
        self,
        profile: ResumeProfile,
    ):

        self.session.resume = profile

        self.session.status = (
            SessionStatus.WAITING_FOR_JOB
        )

        app_logger.success(
            "Resume stored in session."
        )

    # --------------------
    # Job
    # --------------------

    def save_job(
        self,
        profile: JobProfile,
    ):

        self.session.job = profile

        self.session.status = (
            SessionStatus.READY_FOR_MATCHING
        )

        app_logger.success(
            "Job stored in session."
        )

    # --------------------

    def clear(self):
        self.session = UserSession()
        app_logger.info(
            "Session cleared."
        )

session = SessionService()