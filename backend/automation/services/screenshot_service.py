"""
Screenshot Service.

Responsible only for:

- Creating screenshot folders
- Saving screenshots
- Returning saved path
"""

from pathlib import Path


class ScreenshotService:

    ROOT = Path("automation/screenshots")

    @classmethod
    def save(
        cls,
        page,
        application_id: str,
        filename: str,
    ) -> str:

        folder = cls.ROOT / application_id

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = folder / filename

        try:
            # Try capturing full page screenshot
            page.screenshot(
                path=str(path),
                full_page=True,
                timeout=8000,
            )
        except Exception as e:
            from core.logger import app_logger
            app_logger.warning(f"Full page screenshot failed: {e}. Retrying with viewport-only screenshot.")
            try:
                # Fallback to viewport screenshot
                page.screenshot(
                    path=str(path),
                    full_page=False,
                    timeout=5000,
                )
            except Exception as e2:
                app_logger.error(f"Viewport-only screenshot also failed: {e2}")
                return ""

        return str(path)