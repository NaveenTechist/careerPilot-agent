import time

from automation.detector.login_detector import LoginDetector
from automation.services.automation_log_service import AutomationLogService


class LoginManager:

    @staticmethod
    def wait(
        page,
        application_id,
    ):

        if not LoginDetector.detect(page):
            return

        AutomationLogService.log(
            application_id,
            "Login required."
        )

        while LoginDetector.detect(page):

            AutomationLogService.log(
                application_id,
                "Waiting for user login..."
            )

            time.sleep(2)

        AutomationLogService.log(
            application_id,
            "Login completed."
        )