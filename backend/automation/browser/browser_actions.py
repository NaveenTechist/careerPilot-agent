"""
Browser Actions.

Reusable browser operations.

Never write Playwright code
inside AutomationAgent.

AutomationAgent only calls
BrowserActions.
"""

from playwright.sync_api import Page

class BrowserActions:

    # ----------------------------------------

    @staticmethod
    def open_url(
        page: Page,
        url: str,
    ):
        page.goto(
            url,
            wait_until="networkidle",
        )

    # ----------------------------------------

    @staticmethod
    def wait(
        page: Page,
        seconds: int,
    ):
        page.wait_for_timeout(
            seconds * 1000
        )

    # ----------------------------------------

    @staticmethod
    def click(
        page: Page,
        selector: str,
    ):
        page.locator(
            selector
        ).click()

    # ----------------------------------------

    @staticmethod
    def fill(
        page: Page,
        selector: str,
        value: str,
    ):
        page.locator(
            selector
        ).fill(value)

    # ----------------------------------------

    @staticmethod
    def upload(
        page: Page,
        selector: str,
        file_path: str,
    ):
        page.locator(
            selector
        ).set_input_files(
            file_path
        )

    # ----------------------------------------

    @staticmethod
    def exists(
        page: Page,
        selector: str,
    ) -> bool:
        return page.locator(
            selector
        ).count() > 0

    # ----------------------------------------

    @staticmethod
    def text(
        page: Page,
        selector: str,
    ) -> str:
        return page.locator(
            selector
        ).inner_text()

    # ----------------------------------------

    @staticmethod
    def scroll_bottom(
        page: Page,
    ):
        page.evaluate(
            """
            window.scrollTo(
                0,
                document.body.scrollHeight
            );
            """
        )

    # ----------------------------------------

    @staticmethod
    def screenshot(
        page: Page,
        path: str,
    ):
        page.screenshot(
            path=path,
            full_page=True,
        )