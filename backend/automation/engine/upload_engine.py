from automation.browser.browser_actions import BrowserActions
from core.logger import app_logger


class UploadEngine:

    @staticmethod
    def process(
        page,
        resume_path: str,
    ):

        inputs = page.locator("input[type='file']")

        total = inputs.count()

        if total == 0:
            return False

        for i in range(total):

            locator = inputs.nth(i)
            try:
                BrowserActions.upload(
                    locator,
                    resume_path,
                )
                app_logger.success(
                    "Resume uploaded."
                )
                return True
            except Exception:
                continue
        return False