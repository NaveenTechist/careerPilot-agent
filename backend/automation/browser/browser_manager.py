"""
Browser Manager.

Responsible only for:

- Launch Browser
- Create Context
- Create Page
- Close Browser

No automation logic belongs here.
"""

from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # ------------------------------------------

    def launch(self):
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False,      # Change True in Production
            slow_mo=300,
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self.page

    # ------------------------------------------

    def close(self):

        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()