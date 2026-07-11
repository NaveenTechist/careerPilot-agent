"""
Captcha Detector.
"""

from playwright.sync_api import Page

from automation.utils.text_utils import TextUtils


class CaptchaDetector:

    KEYWORDS = [

        "captcha",

        "i'm not a robot",

        "verify you are human",

        "recaptcha",

        "hcaptcha",

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