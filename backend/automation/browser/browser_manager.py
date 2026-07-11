"""
Browser Manager.

Responsible only for:

- Launch Browser
- Create Context
- Create Page
- Close Browser
"""

from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

from core.logger import app_logger


class BrowserManager:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # --------------------------------------------------

    def launch(self) -> Page:

        app_logger.info("Launching Chromium browser.")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False,      # True in Production
            slow_mo=300,
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        app_logger.success("Browser launched.")

        return self.page

    # --------------------------------------------------

    def close(self):

        app_logger.info("Closing browser.")
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        app_logger.success("Browser closed.")