from playwright.sync_api import Page

from automation.utils.text_utils import TextUtils


class SuccessDetector:

    KEYWORDS = [

        "application submitted",

        "application complete",

        "thank you",

        "your application has been received",

        "successfully applied",

        "confirmation",

    ]

    @classmethod
    def detect(
        cls,
        page: Page,
    ) -> bool:

        body = TextUtils.normalize(

            page.locator("body").inner_text()

        )

        return any(

            word in body

            for word in cls.KEYWORDS

        )