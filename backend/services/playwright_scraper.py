"""
Playwright Scraper

Responsibilities
----------------
1. Open JavaScript-rendered pages.
2. Accept cookie banners when possible.
3. Extract the largest visible content.
4. Return clean text.

This class should NEVER:
- Parse jobs
- Call Gemini
- Match resumes

Single Responsibility Principle.
"""

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

from core.config import settings
from core.exceptions import JobScrapingError
from core.logger import app_logger


JOB_SELECTORS = [
    "main",
    "[role='main']",
    ".job-description",
    ".jobDescription",
    ".job-details",
    ".description",
    "article",
    ".content",
    "#content",
    "body",
]


COOKIE_BUTTONS = [
    "Accept",
    "Accept All",
    "Accept all",
    "I Agree",
    "Agree",
    "Allow",
    "Allow All",
]


class PlaywrightScraper:
    """
    Scrapes JavaScript-rendered pages using Playwright.
    """

    def scrape(
        self,
        url: str,
    ) -> str:

        app_logger.info(f"Launching Playwright for {url}")

        browser = None

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(
                    headless=settings.HEADLESS_BROWSER,
                )
                try:
                    context = browser.new_context()
                    page = context.new_page()

                    for attempt in range(3):
                        try:
                            page.goto(
                                url,
                                wait_until="domcontentloaded",
                                timeout=settings.PLAYWRIGHT_TIMEOUT,
                            )
                            break
                        except Exception:
                            app_logger.warning(
                                f"Navigation failed. Retry {attempt + 1}/3"
                            )
                            continue
                        if attempt == 2:
                            raise
                    page.wait_for_timeout(2000)
                    self._accept_cookies(page)
                    page.wait_for_load_state("networkidle")
                    page_text = self._extract_text(page)

                    if len(page_text) < settings.MIN_JOB_TEXT_LENGTH:
                        raise JobScrapingError("Insufficient page content extracted.")
                    app_logger.success(
                        f"Playwright extracted {len(page_text)} characters."
                    )
                    print(page_text)
                    return page_text
                except Exception as exc:
                    app_logger.exception("Playwright scraping failed.")

                    raise JobScrapingError("Unable to scrape page.") from exc

        except PlaywrightTimeoutError as exc:
            app_logger.exception("Playwright timeout.")

            raise JobScrapingError("Page load timed out.") from exc

        except Exception as exc:
            app_logger.exception("Playwright scraping failed.")

            raise JobScrapingError("Unable to scrape page.") from exc

    def _accept_cookies(
        self,
        page,
    ) -> None:
        """
        Try clicking common cookie banners.

        Ignore failures because many pages
        simply don't have one.
        """

        for button_text in COOKIE_BUTTONS:
            try:
                page.get_by_text(
                    button_text,
                    exact=False,
                ).click(
                    timeout=1000,
                )

                app_logger.info(f"Cookie banner accepted: {button_text}")

                return

            except Exception:
                continue

    def _extract_text(
        self,
        page,
    ) -> str:
        """
        Extract the largest visible content
        from the page.
        """
        best_text = ""
        for selector in JOB_SELECTORS:
            try:
                locator = page.locator(selector)
                if locator.count() == 0:
                    continue
                candidate = (locator.first.inner_text()).strip()
                if len(candidate) > len(best_text):
                    best_text = candidate
            except Exception:
                continue
        return best_text
