"""
Automation Agent.

Coordinates browser automation.
"""

from automation.browser.browser_manager import BrowserManager
from automation.browser.browser_actions import BrowserActions
from automation.services.screenshot_service import ScreenshotService
from automation.services.automation_log_service import AutomationLogService

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
            f"Starting automation: {application_id}"
        )

        AutomationLogService.clear(
            application_id
        )

        AutomationLogService.log(
            application_id,
            "Automation started."
        )

        application = self.application_repository.get_by_id(
            application_id
        )

        if application is None:
            raise Exception("Application not found.")

        job = self.job_repository.get_by_id(
            application.job_id
        )

        if job is None:
            raise Exception("Job not found.")

        browser = BrowserManager()

        page = browser.launch()

        try:
            self.application_repository.update_status(
                application_id,
                ApplicationStatus.PROCEEDED,
            )
            AutomationLogService.log(
                application_id,
                "Opening job page."
            )
            BrowserActions.goto(
                page,
                job.application_url,
            )
            ScreenshotService.save(
                page,
                application_id,
                "001_job_page.png",
            )
            AutomationLogService.log(
                application_id,
                "Job page screenshot captured."
            )
            self.application_repository.update_status(
                application_id,
                ApplicationStatus.COMPLETED,
            )
            AutomationLogService.log(
                application_id,
                "Automation completed."
            )
            return {
                "success": True,
            }
        except Exception as e:
            self.application_repository.update_status(
                application_id,
                ApplicationStatus.CANCELLED,
            )
            AutomationLogService.log(
                application_id,
                f"Automation failed: {e}"
            )
            raise
        finally:
            browser.close()
            AutomationLogService.log(
                application_id,
                "Browser closed."
            )