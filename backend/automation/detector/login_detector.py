from playwright.sync_api import Page


class LoginDetector:

    LOGIN_URLS = [

        "/login",

        "/signin",

        "/auth",

        "/oauth",

    ]

    @classmethod
    def detect(
        cls,
        page: Page,
    ) -> bool:

        url = page.url.lower()

        if any(x in url for x in cls.LOGIN_URLS):

            return True

        password = page.locator(
            "input[type='password']:visible"
        )

        if password.count() > 0:
            return True
        email = page.locator(
            "input[type='email']:visible"
        )
        if email.count() > 0:
            return True
        login_buttons = page.locator(
            """
            button:has-text("Sign In"),
            button:has-text("Login"),
            button:has-text("Log In"),
            button:has-text("Continue")
            """
        )
        if login_buttons.count() > 0:
            return True
        return False