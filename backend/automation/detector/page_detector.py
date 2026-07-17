"""
Page Detector.

Classifies the current browser page into a PageType
so the automation agent can take the correct action
without blindly iterating over elements.

Detection order matters — we check from most specific
to least specific to avoid false positives:

    1. LOADING   — page not ready yet, wait
    2. ERROR     — dead end, stop early
    3. SUCCESS   — application done
    4. LOGIN     — needs user auth
    5. REVIEW    — summary before submit
    6. FORM      — fillable fields present
    7. APPLY     — apply button visible (landing)
    8. LANDING   — job description visible
    9. UNKNOWN   — fallback
"""

from playwright.sync_api import Page

from automation.models.page_type import PageType
from automation.utils.text_utils import TextUtils
from core.logger import app_logger


class PageDetector:

    # --------------------------------------------------
    # Loading indicators
    # --------------------------------------------------

    LOADING_SELECTORS = [
        "[class*='spinner']",
        "[class*='loading']",
        "[class*='skeleton']",
        "[class*='loader']",
        "[role='progressbar']",
        ".lds-ring",
        ".lds-spinner",
        "[class*='shimmer']",
        "[aria-busy='true']",
    ]

    # --------------------------------------------------
    # Error page keywords (body text)
    # --------------------------------------------------

    ERROR_KEYWORDS = [
        "this job is no longer available",
        "this position has been filled",
        "job has been closed",
        "job no longer accepting",
        "this requisition is no longer active",
        "page not found",
        "404",
        "access denied",
        "forbidden",
        "expired link",
        "link has expired",
        "this page isn't working",
        "application deadline has passed",
        "no longer accepting applications",
        "this role has been filled",
    ]

    # --------------------------------------------------
    # Success / confirmation keywords (body text)
    # --------------------------------------------------

    SUCCESS_KEYWORDS = [
        "application submitted",
        "application received",
        "application complete",
        "thank you for applying",
        "thank you for your application",
        "thanks for applying",
        "successfully applied",
        "successfully submitted",
        "your application has been received",
        "your application has been submitted",
        "we have received your application",
        "submission complete",
        "application confirmation",
    ]

    # --------------------------------------------------
    # Review / preview page keywords
    # --------------------------------------------------

    REVIEW_KEYWORDS = [
        "review your application",
        "review and submit",
        "review application",
        "review & submit",
        "preview application",
        "application summary",
        "confirm and submit",
        "please review",
        "verify your information",
    ]

    # --------------------------------------------------
    # Login detection: URL patterns
    # --------------------------------------------------

    LOGIN_URL_PATTERNS = [
        "/login",
        "/signin",
        "/sign-in",
        "/auth",
        "/oauth",
        "/sso",
        "/account/login",
        "/sessions/new",
    ]

    # --------------------------------------------------
    # Apply button keywords
    # --------------------------------------------------

    APPLY_KEYWORDS = [
        "apply",
        "apply now",
        "easy apply",
        "quick apply",
        "start application",
        "continue application",
        "submit application",
        "submit resume",
        "apply for this job",
        "apply for this position",
        "apply on company site",
    ]

    APPLY_IGNORE = [
        "save",
        "share",
        "login",
        "log in",
        "sign in",
        "register",
        "cancel",
        "close",
        "back",
    ]

    # ==========================================================================
    # PUBLIC API
    # ==========================================================================

    @classmethod
    def detect(cls, page: Page) -> PageType:
        """
        Classify the current page state.

        Returns the most specific PageType
        that matches the current DOM.
        """
        try:
            # 1. Loading — check first so we wait
            if cls._is_loading(page):
                app_logger.debug("Page classified as LOADING.")
                return PageType.LOADING

            # Grab body text once (expensive DOM call)
            body_text = cls._get_body_text(page)

            # 2. Error — dead end
            if cls._is_error(body_text):
                app_logger.info("Page classified as ERROR.")
                return PageType.ERROR

            # 3. Success — we're done
            if cls._is_success(body_text):
                app_logger.info("Page classified as SUCCESS.")
                return PageType.SUCCESS

            # 4. Login — needs auth
            if cls._is_login(page):
                app_logger.info("Page classified as LOGIN.")
                return PageType.LOGIN

            # 5. Review — summary screen
            if cls._is_review(page, body_text):
                app_logger.info("Page classified as REVIEW.")
                return PageType.REVIEW

            # 6. Form — fillable fields
            if cls._is_form(page):
                app_logger.info("Page classified as FORM.")
                return PageType.FORM

            # 7. Apply — start button present
            if cls._has_apply_button(page):
                app_logger.info("Page classified as APPLY.")
                return PageType.APPLY

            # 8. Landing — job description present
            if cls._is_landing(body_text):
                app_logger.info("Page classified as LANDING.")
                return PageType.LANDING

            # 9. Unknown
            app_logger.warning("Page classified as UNKNOWN.")
            return PageType.UNKNOWN

        except Exception as exc:
            app_logger.exception(f"PageDetector error: {exc}")
            return PageType.UNKNOWN

    # ==========================================================================
    # PRIVATE HELPERS
    # ==========================================================================

    @classmethod
    def _get_body_text(cls, page: Page) -> str:
        """Extract and normalize full body text."""
        try:
            raw = page.locator("body").inner_text(timeout=5000)
            return TextUtils.normalize(raw)
        except Exception:
            return ""

    # --------------------------------------------------
    # LOADING
    # --------------------------------------------------

    @classmethod
    def _is_loading(cls, page: Page) -> bool:
        """
        Detect loading state by checking for
        spinners, skeletons, loaders, and AJAX overlays.
        """
        for selector in cls.LOADING_SELECTORS:
            try:
                locator = page.locator(f"{selector}:visible")
                if locator.count() > 0:
                    return True
            except Exception:
                continue

        # Check if document is still loading via JS
        try:
            ready_state = page.evaluate("document.readyState")
            if ready_state == "loading":
                return True
        except Exception:
            pass

        return False

    # --------------------------------------------------
    # ERROR
    # --------------------------------------------------

    @classmethod
    def _is_error(cls, body_text: str) -> bool:
        """Detect error / dead-end pages."""
        return any(
            keyword in body_text
            for keyword in cls.ERROR_KEYWORDS
        )

    # --------------------------------------------------
    # SUCCESS
    # --------------------------------------------------

    @classmethod
    def _is_success(cls, body_text: str) -> bool:
        """Detect application confirmation pages."""
        return any(
            keyword in body_text
            for keyword in cls.SUCCESS_KEYWORDS
        )

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    @classmethod
    def _is_login(cls, page: Page) -> bool:
        """
        Detect login/auth pages via URL patterns
        and visible password/email fields.
        """
        url = page.url.lower()

        if any(pattern in url for pattern in cls.LOGIN_URL_PATTERNS):
            return True

        # Visible password field is the strongest login signal
        try:
            password_fields = page.locator("input[type='password']:visible")
            if password_fields.count() > 0:
                return True
        except Exception:
            pass

        # Sign-in / Login buttons combined with minimal form fields
        try:
            login_buttons = page.locator(
                "button:has-text('Sign In'),"
                "button:has-text('Log In'),"
                "button:has-text('Login'),"
                "input[type='submit'][value*='Sign' i],"
                "input[type='submit'][value*='Log' i]"
            )
            if login_buttons.count() > 0:
                # Only classify as login if there aren't many
                # other form fields (to avoid false positives
                # on forms that also have a login link)
                all_inputs = page.locator(
                    "input:visible:not([type='hidden']):not([type='submit'])"
                )
                if all_inputs.count() <= 4:
                    return True
        except Exception:
            pass

        return False

    # --------------------------------------------------
    # REVIEW
    # --------------------------------------------------

    @classmethod
    def _is_review(cls, page: Page, body_text: str) -> bool:
        """
        Detect review/preview pages.

        A review page typically has:
        - Review-related keywords in headings or body
        - A submit button present
        - Very few or no editable input fields
        """
        has_review_text = any(
            keyword in body_text
            for keyword in cls.REVIEW_KEYWORDS
        )

        if not has_review_text:
            return False

        # Confirm: has a submit button
        try:
            submit_buttons = page.locator(
                "button:has-text('Submit'),"
                "input[type='submit'],"
                "button:has-text('Confirm')"
            )
            if submit_buttons.count() > 0:
                return True
        except Exception:
            pass

        return False

    # --------------------------------------------------
    # FORM
    # --------------------------------------------------

    @classmethod
    def _is_form(cls, page: Page) -> bool:
        """
        Detect active form pages by checking
        for visible, editable input fields.
        """
        try:
            editable_fields = page.locator(
                "input:visible:not([type='hidden'])"
                ":not([type='submit'])"
                ":not([type='button']),"
                "textarea:visible,"
                "select:visible"
            )
            return editable_fields.count() > 0
        except Exception:
            return False

    # --------------------------------------------------
    # APPLY BUTTON
    # --------------------------------------------------

    @classmethod
    def _has_apply_button(cls, page: Page) -> bool:
        """Detect if an Apply-type button is on the page."""
        try:
            elements = page.locator(
                "button,a,input[type='submit'],"
                "input[type='button'],[role='button']"
            )
            count = elements.count()

            for i in range(count):
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

                if any(word in text for word in cls.APPLY_IGNORE):
                    continue

                if any(word in text for word in cls.APPLY_KEYWORDS):
                    return True
        except Exception:
            pass

        return False

    # --------------------------------------------------
    # LANDING
    # --------------------------------------------------

    @classmethod
    def _is_landing(cls, body_text: str) -> bool:
        """
        Detect job description / landing pages.

        Landing pages typically contain job-related
        keywords and have substantial text content.
        """
        landing_signals = [
            "job description",
            "responsibilities",
            "requirements",
            "qualifications",
            "about the role",
            "about this role",
            "what you'll do",
            "what we're looking for",
            "who you are",
            "your responsibilities",
            "key responsibilities",
            "minimum qualifications",
            "preferred qualifications",
            "benefits",
            "about us",
            "about the company",
        ]

        matches = sum(
            1 for signal in landing_signals
            if signal in body_text
        )

        # At least 2 signals = likely a job posting
        return matches >= 2
