"""
Fill Action.
"""

from playwright.sync_api import Page


class FillAction:

    @staticmethod
    def fill(

        page: Page,

        selector: str,

        value: str,

    ):

        page.locator(

            selector

        ).fill(

            value

        )