"""
Resume Uploader.
"""

from core.logger import app_logger
from automation.browser.browser_actions import BrowserActions


class ResumeUploader:

    @staticmethod
    def upload(
        page,
        resume_path,
    ):

        upload = page.locator(
            "input[type='file']"
        )

        if upload.count() == 0:

            app_logger.info(
                "Resume upload field not found."
            )

            return

        BrowserActions.upload(
            upload.first,
            resume_path,
        )

        app_logger.success(
            "Resume uploaded."
        )