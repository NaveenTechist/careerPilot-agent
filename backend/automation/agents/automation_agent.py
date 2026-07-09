"""
Automation Agent.

Coordinates browser automation.

Responsibilities

- Load Application
- Open Browser
- Visit Job URL
- Capture Proof
- Update Status
- Close Browser
"""

from automation.browser.browser_manager import BrowserManager
from automation.services.screenshot_service import ScreenshotService
from automation.services.automation_log_service import AutomationLogService
from repositories.application_repository import ApplicationRepository
from models.db.application_entity import ApplicationStatus
from core.logger import app_logger



class AutomationAgent:

    def __init__(
        self,
        application_repository,
        resume_repository,
        job_repository,
        match_repository,

    ):
        self.application_repository = application_repository
        self.resume_repository = resume_repository
        self.job_repository = job_repository
        self.match_repository = match_repository
    # --------------------------------------------------
    def process(
        self,
        application_id: str,
    ):

        app_logger.info(
            "Automation started."
        )

        application = self.repository.get_by_id(
            application_id
        )

        if application is None:

            raise Exception(
                "Application not found."
            )

        browser = BrowserManager()

        page = browser.launch()

        try:

            AutomationLogService.log(
                application_id,
                "Browser launched."
            )

            self.repository.update_status(
                application_id,
                ApplicationStatus.AUTOMATION_RUNNING,
            )

            job = application.job

            AutomationLogService.log(
                application_id,
                f"Opening {job.application_url}"
            )

            page.goto(
                job.application_url,
                wait_until="networkidle",
            )

            ScreenshotService.save(
                page,
                application_id,
                "001_job_page.png",
            )

            AutomationLogService.log(
                application_id,
                "Screenshot captured."
            )

            self.repository.update_status(
                application_id,
                ApplicationStatus.SUBMITTED,
            )

            AutomationLogService.log(
                application_id,
                "Automation completed."
            )

            return {
                "success": True,
            }

        finally:

            browser.close()

            AutomationLogService.log(
                application_id,
                "Browser closed."
            )