"""
Field Filler.
"""

from automation.browser.browser_actions import BrowserActions
from core.logger import app_logger


class FieldFiller:

    @staticmethod
    def fill(
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):

            return

        try:

            BrowserActions.fill(
                field.locator,
                value,
            )

            app_logger.success(
                f"Filled {field.label}"
            )

        except Exception:

            app_logger.exception(
                f"Unable to fill {field.label}"
            )