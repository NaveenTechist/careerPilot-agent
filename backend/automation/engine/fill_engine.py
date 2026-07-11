"""
Fill Engine.

Fills one field.
"""

from automation.browser.browser_actions import BrowserActions


class FillEngine:

    @staticmethod
    def fill(
        page,
        field,
        value,
    ):
        if value is None:
            return
        BrowserActions.fill(
            page,
            field.selector,
            str(value),
        )