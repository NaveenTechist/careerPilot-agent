from services.http_scraper import HttpScraper

from .strategy_result import StrategyResult
from .base_strategy import BaseExtractionStrategy


class HttpStrategy(BaseExtractionStrategy):
    def __init__(self):
        self.scraper = HttpScraper()

    def extract(
        self,
        url: str,
    ) -> StrategyResult:
        try:
            text = self.scraper.scrape(url)
            return StrategyResult(
                success=True,
                strategy="HTTP",
                content=text,
            )
        except Exception as exc:
            return StrategyResult(
                success=False,
                strategy="HTTP",
                error=str(exc),
            )
