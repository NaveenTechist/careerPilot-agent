"""
Login Detector.
"""

from playwright.sync_api import Page

from automation.utils.text_utils import TextUtils


class LoginDetector:

    KEYWORDS = [

        "sign in",

        "login",

        "log in",

        "continue with google",

        "continue with linkedin",

        "email",

        "password",

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

            key in body

            for key in cls.KEYWORDS

        )