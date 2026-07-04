from core.logger import app_logger

from .http_strategy import HttpStrategy

from .playwright_strategy import (
    PlaywrightStrategy,
)


class ExtractionEngine:
    def __init__(self):
        self.strategies = [
            HttpStrategy(),
            PlaywrightStrategy(),
        ]

    def extract(
        self,
        url: str,
    ) -> str:

        for strategy in self.strategies:
            app_logger.info(f"Trying {strategy.__class__.__name__}")
            result = strategy.extract(url)

            if result.success:
                app_logger.success(f"{result.strategy} succeeded.")
                return result.content
            app_logger.warning(f"{result.strategy} failed.")
        raise RuntimeError("All extraction strategies failed.")


# JobAgent
#       │
#       ▼
# ExtractionEngine
#       │
#       ├── HTTP
#       ├── Playwright
#       ├── JSON-LD
#       ├── API Discovery
#       ├── Stealth
#       ├── Site Adapter
#       └── OCR
