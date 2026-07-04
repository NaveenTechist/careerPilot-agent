class PlaywrightStrategy(BaseExtractionStrategy):
    def __init__(self):

        self.scraper = PlaywrightScraper()

    def extract(
        self,
        url: str,
    ) -> StrategyResult:

        try:
            text = self.scraper.scrape(url)

            return StrategyResult(
                success=True,
                strategy="PLAYWRIGHT",
                content=text,
            )

        except Exception as exc:
            return StrategyResult(
                success=False,
                strategy="PLAYWRIGHT",
                error=str(exc),
            )
