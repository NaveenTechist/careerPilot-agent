"""
Job Scraper Service.
Coordinates scraping strategies.
Workflow
HTTP
↓
Success?
↓
YES
↓
Return
↓
NO
↓
Playwright
↓
Return
"""

from services.http_scraper import HttpScraper
from services.playwright_scraper import (
    PlaywrightScraper,
)

from core.logger import app_logger
from core.exceptions import JobScrapingError


class JobScraperService:
    def __init__(self):
        self.http = HttpScraper()

        self.browser = PlaywrightScraper()

    def scrape(
        self,
        url: str,
    ) -> str:
        try:
            app_logger.info("Trying HTTP strategy.")
            return self.http.scrape(url)

        except JobScrapingError:
            app_logger.warning("HTTP strategy failed.")

        app_logger.info("Trying Playwright strategy.")

        return self.browser.scrape(url)
