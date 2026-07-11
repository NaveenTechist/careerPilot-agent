"""
Apply Action.
"""

from automation.detector.apply_detector import ApplyDetector
from automation.browser.browser_actions import BrowserActions

from core.logger import app_logger


class ApplyAction:

    @staticmethod
    def execute(
        page,
    ) -> bool:

        app_logger.info(
            "Searching Apply button."
        )

        button = ApplyDetector.detect(
            page
        )

        if button is None:

            app_logger.error(
                "Apply button not found."
            )

            return False

        BrowserActions.click(
            button
        )
        BrowserActions.wait(
            page
        )
        app_logger.success(
            "Apply button clicked."
        )
        return True