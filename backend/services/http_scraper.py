"""
HTTP Scraper Service.

Downloads job pages using a lightweight HTTP request.

Use this first because it is much faster than
running a full browser.

If HTTP cannot extract meaningful content,
the JobScraperService will automatically
fallback to Playwright.
"""

from bs4 import BeautifulSoup
import requests

from core.logger import app_logger
from core.exceptions import JobScrapingError


class HttpScraper:
    """
    Lightweight HTML scraper.

    Responsibility:
        Download HTML
        Remove unnecessary tags
        Return visible text
    """

    TIMEOUT = 15

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 "
            "(KHTML, like Gecko)"
            " Chrome/137.0 Safari/537.36"
        )
    }

    def scrape(
        self,
        url: str,
    ) -> str:

        app_logger.info(f"Fetching job page via HTTP: {url}")

        try:
            response = requests.get(
                url,
                headers=self.HEADERS,
                timeout=self.TIMEOUT,
            )

            response.raise_for_status()

        except requests.RequestException as exc:
            app_logger.exception("HTTP request failed.")

            raise JobScrapingError("Unable to download job page.") from exc

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Remove unnecessary tags

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "footer",
                "header",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        if len(text) < 500:
            app_logger.warning("Very little text extracted from HTTP page.")

            raise JobScrapingError("Insufficient content.")

        app_logger.success("HTTP scraping completed.")

        return text
