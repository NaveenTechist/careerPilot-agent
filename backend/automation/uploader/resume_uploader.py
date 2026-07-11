"""
Resume Uploader.

Responsible for uploading
resume files.
"""

from playwright.sync_api import Page

from core.logger import app_logger


class ResumeUploader:

    @staticmethod
    def upload(
        page: Page,
        resume_path: str,
    ) -> bool:

        app_logger.info(
            "Searching resume upload field."
        )

        upload = page.locator(
            "input[type='file']"
        ).first

        try:

            upload.set_input_files(
                resume_path
            )

            app_logger.success(
                "Resume uploaded successfully."
            )

            return True

        except Exception:

            app_logger.exception(
                "Resume upload failed."
            )

            return False