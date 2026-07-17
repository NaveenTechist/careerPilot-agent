"""
Browser Actions.

Common Playwright actions.
"""

from playwright.sync_api import Page
from core.logger import app_logger


class BrowserActions:

    @staticmethod
    def goto(
        page: Page,
        url: str,
    ):

        app_logger.info(
            f"Opening {url}"
        )

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        app_logger.success(
            "Job page loaded."
        )

    # -----------------------------------------

    @staticmethod
    def click(
        locator,
    ):

        locator.scroll_into_view_if_needed()

        locator.click()

    # -----------------------------------------

    @staticmethod
    def fill(
        locator,
        value: str,
    ):

        locator.scroll_into_view_if_needed()

        locator.fill(
            str(value)
        )

    # -----------------------------------------

    @staticmethod
    def upload(
        locator,
        file_path: str,
    ):

        locator.set_input_files(
            file_path
        )

    # -----------------------------------------

    @staticmethod
    def wait(
        page: Page,
    ):

        page.wait_for_load_state(
            "domcontentloaded"
        )