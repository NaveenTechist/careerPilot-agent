"""
Automation Agent.

Coordinates browser automation.
"""

from automation.browser.browser_manager import BrowserManager
from automation.browser.browser_actions import BrowserActions
from automation.services.screenshot_service import ScreenshotService
from automation.actions.apply_action import ApplyAction
from automation.services.automation_log_service import AutomationLogService
from automation.engine.form_engine import FormEngine
from automation.detector.login_detector import LoginDetector
from automation.detector.captcha_detector import CaptchaDetector
from automation.services.network_service import NetworkService
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
        AutomationEventService.publish(
            application_id,
            step="browser",
            message="Launching Browser",
            progress=5,
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
            AutomationEventService.publish(
                application_id,
                step="job",
                message="Opening Job Page",
                progress=15,
            )
            BrowserActions.goto(
                page,
                job.application_url,
            )
            ApplyAction.execute(page)
            ScreenshotService.save(
                page,
                application_id,
                "001_job_page.png",
            )
            AutomationLogService.log(
                application_id,
                "Job page screenshot captured."
            )
            AutomationEventService.publish(
                application_id,
                step="apply",
                message="Clicking Apply",
                progress=30,
            )
            while True:
                AutomationLogService.log(application_id, "Checking login...")
                app_logger.info(
                    "Checking login..."
                )
                AutomationEventService.publish(
                    application_id,
                    step="login",
                    message="Waiting Login",
                    progress=40,
                )

                if not NetworkService.is_online():

                    AutomationLogService.log(
                        application_id,
                        "Internet connection lost."
                    )

                # self.application_repository.update_status(
                #     application_id,
                #     ApplicationStatus.WAITING_NETWORK,
                # )

                while not NetworkService.is_online():

                    time.sleep(3)

                    AutomationLogService.log(
                        application_id,
                        "Internet restored."
                    )

                if LoginDetector.detect(page):
                    AutomationLogService.log(application_id, "Login required.")
                    app_logger.info(
                        "Login detected."
                    )
                    AutomationEventService.publish(
                        application_id,
                        step="login",
                        message="Waiting Login",
                        progress=40,
                    )
                    # wait user
                    continue
                AutomationLogService.log(application_id, "Checking captcha...")
                app_logger.info(
                    "Checking captcha..."
                )
                if CaptchaDetector.detect(page):
                    AutomationLogService.log(application_id, "Captcha detected.")
                    app_logger.info(
                        "Captcha detected."
                    )
                    # wait user
                    continue
                AutomationLogService.log(application_id, "Scanning form...")
                FormEngine.process(
                    page,
                    application,
                )
                AutomationLogService.log(application_id, "Navigating...")
                app_logger.info(
                    "Navigating..."
                )
                finished = NavigationEngine.process(
                    page,
                )
                if finished:
                    AutomationLogService.log(application_id, "Navigation completed.")
                    app_logger.info(
                        "Navigation completed."
                    )
                    break
                ScreenshotService.save(
                    page,
                    application_id,
                    f"00{page}.png",
                )
                app_logger.info(
                    f"Screenshot captured: 00{page}.png"
                )
                AutomationLogService.log(
                    application_id,
                    f"Screenshot captured: 00{page}.png"
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