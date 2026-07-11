"""
Universal Apply Detector.
"""

from playwright.sync_api import Locator
from playwright.sync_api import Page

from automation.utils.text_utils import TextUtils


class ApplyDetector:

    KEYWORDS = [

        "apply",

        "easy apply",

        "quick apply",

        "apply now",

        "start application",

        "continue application",

        "submit application",

        "submit resume",

        "apply for this job",

    ]

    IGNORE = [

        "save",

        "share",

        "login",

        "log in",

        "register",

        "cancel",

        "close",

        "back",

    ]

    @classmethod
    def detect(

        cls,

        page: Page,

    ) -> Locator | None:

        elements = page.locator(

            "button,a,input[type='submit'],input[type='button'],[role='button']"

        )

        total = elements.count()

        for i in range(total):

            element = elements.nth(i)

            try:

                text = TextUtils.normalize(

                    element.inner_text()

                )

            except Exception:

                try:

                    text = TextUtils.normalize(

                        element.get_attribute("value")

                    )

                except Exception:

                    continue

            if not text:

                continue

            if any(

                word in text

                for word in cls.IGNORE

            ):

                continue

            if any(

                word in text

                for word in cls.KEYWORDS

            ):

                return element

        return None