from playwright.sync_api import Locator
from playwright.sync_api import Page

from automation.utils.text_utils import TextUtils


class NextDetector:

    KEYWORDS = [

        "next",

        "continue",

        "continue application",

        "save and continue",

        "proceed",

    ]

    @classmethod
    def detect(
        cls,
        page: Page,
    ) -> Locator | None:

        buttons = page.locator(
            "button,a,input[type='submit']"
        )

        total = buttons.count()

        for i in range(total):

            button = buttons.nth(i)

            try:

                text = TextUtils.normalize(
                    button.inner_text()
                )

            except Exception:

                continue

            if any(
                key in text
                for key in cls.KEYWORDS
            ):
                return button

        return None