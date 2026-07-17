"""
Automation Agent.

State-machine-driven browser automation.

Instead of blindly checking for elements on every
iteration, the agent classifies the current page
using PageDetector and takes the appropriate action
for each PageType.

State Machine Flow:
    LOADING      → wait and re-detect
    ERROR        → fail with message
    SUCCESS      → mark completed
    LOGIN        → pause for user authentication
    APPLY        → click apply button
    FORM         → parse fields, fill, navigate
    REVIEW       → screenshot, prepare for submit
    LANDING      → look for apply button
    WAITING_USER → pause for user input (future)
    UNKNOWN      → retry with wait, then fail
"""

import time

from automation.browser.browser_manager import BrowserManager
from automation.browser.browser_actions import BrowserActions
from automation.services.screenshot_service import ScreenshotService
from automation.services.automation_log_service import AutomationLogService
from automation.services.network_service import NetworkService
from automation.detector.page_detector import PageDetector
from automation.detector.captcha_detector import CaptchaDetector
from automation.models.page_type import PageType
from automation.actions.apply_action import ApplyAction
from automation.parser.field_parser import FieldParser
from automation.matcher.answer_matcher import AnswerMatcher
from automation.filler.field_filler import FieldFiller
from automation.engine.upload_engine import UploadEngine
from automation.engine.navigation_engine import NavigationEngine
from automation.navigation.navigation_result import NavigationResult
from models.db.application_entity import ApplicationStatus
from core.logger import app_logger
from automation.models.field_type import FieldType


class AutomationAgent:

    # Maximum number of state transitions before
    # we assume the automation is stuck.
    MAX_STEPS = 30

    # Maximum consecutive LOADING states before
    # we give up waiting.
    MAX_LOADING_WAITS = 10

    # Maximum consecutive UNKNOWN states before
    # we declare failure.
    MAX_UNKNOWN_RETRIES = 3

    # Seconds to wait between loading checks.
    LOADING_WAIT_SECONDS = 2

    # Seconds to wait for login.
    LOGIN_POLL_SECONDS = 3

    # --------------------------------------------------

    def __init__(
        self,
        application_repository,
        resume_repository,
        job_repository,
        match_repository,
    ):
        self.application_repository = application_repository
        self.resume_repository = resume_repository
        self.job_repository = job_repository
        self.match_repository = match_repository

    # ==========================================================================
    # MAIN ENTRY POINT
    # ==========================================================================

    def process(
        self,
        application_id: str,
    ):
        app_logger.info(f"Starting automation: {application_id}")

        AutomationLogService.clear(application_id)
        AutomationLogService.log(application_id, "Automation started.")

        # -----------------------------------------------
        # Load application data
        # -----------------------------------------------
        application = self.application_repository.get_by_id(application_id)
        if application is None:
            raise Exception("Application not found.")

        resume = self.resume_repository.get_by_id(application.resume_id)
        if resume is None:
            raise Exception("Resume not found.")

        job = self.job_repository.get_by_id(application.job_id)
        if job is None:
            raise Exception("Job not found.")

        # -----------------------------------------------
        # Launch browser
        # -----------------------------------------------
        browser = BrowserManager()
        page = browser.launch()

        try:
            self.application_repository.update_status(
                application_id,
                ApplicationStatus.PROCEEDED,
            )

            # -------------------------------------------
            # Navigate to job URL
            # -------------------------------------------
            AutomationLogService.log(application_id, "Opening job page.")
            BrowserActions.goto(page, job.application_url)

            ScreenshotService.save(page, application_id, "001_initial_page.png")
            AutomationLogService.log(application_id, "Initial page screenshot captured.")

            # -------------------------------------------
            # State machine loop
            # -------------------------------------------
            self._run_state_machine(
                page=page,
                application_id=application_id,
                resume=resume,
            )

            # -------------------------------------------
            # Mark completed
            # -------------------------------------------
            self.application_repository.update_status(
                application_id,
                ApplicationStatus.COMPLETED,
            )
            AutomationLogService.log(application_id, "Automation completed successfully.")

            return {"success": True}

        except Exception as e:
            self.application_repository.update_status(
                application_id,
                ApplicationStatus.CANCELLED,
            )
            AutomationLogService.log(application_id, f"Automation failed: {e}")
            raise

        finally:
            browser.close()
            AutomationLogService.log(application_id, "Browser closed.")

    # ==========================================================================
    # STATE MACHINE
    # ==========================================================================

    def _run_state_machine(
        self,
        page,
        application_id: str,
        resume,
    ):
        """
        Core automation loop.

        On each iteration:
            1. Check network connectivity
            2. Detect current page type
            3. Execute the handler for that page type
            4. Repeat until SUCCESS or failure
        """
        step = 0
        loading_count = 0
        unknown_count = 0
        screenshot_counter = 2  # 001 already taken
        resume_uploaded = False

        while step < self.MAX_STEPS:
            step += 1
            app_logger.info(f"Step {step}/{self.MAX_STEPS}")

            # -------------------------------------------
            # Network check
            # -------------------------------------------
            self._wait_for_network(application_id)

            # -------------------------------------------
            # Captcha check
            # -------------------------------------------
            if CaptchaDetector.detect(page):
                AutomationLogService.log(
                    application_id,
                    "CAPTCHA detected. Waiting for user to solve..."
                )
                time.sleep(5)
                continue

            # -------------------------------------------
            # Modal / Overlay check & handle
            # -------------------------------------------
            from automation.detector.modal_detector import ModalDetector
            modal_status = ModalDetector.detect_and_handle(page, application_id)
            if modal_status == "WAITING_USER":
                AutomationLogService.log(
                    application_id,
                    "Blocking modal/overlay remains active. Pausing for user interaction."
                )
                raise Exception("Automation paused: active modal or overlay requires user interaction.")

            # -------------------------------------------
            # Classify current page
            # -------------------------------------------
            page_type = PageDetector.detect(page)
            AutomationLogService.log(
                application_id,
                f"Page detected: {page_type.value}"
            )

            # -------------------------------------------
            # Handle each page type
            # -------------------------------------------

            match page_type:

                # ======================================
                # LOADING
                # ======================================
                case PageType.LOADING:
                    loading_count += 1
                    if loading_count > self.MAX_LOADING_WAITS:
                        AutomationLogService.log(
                            application_id,
                            "Page stuck in loading state. Proceeding anyway."
                        )
                        loading_count = 0
                        # Fall through to re-detect
                    else:
                        AutomationLogService.log(
                            application_id,
                            f"Page loading... ({loading_count}/{self.MAX_LOADING_WAITS})"
                        )
                        time.sleep(self.LOADING_WAIT_SECONDS)
                    continue

                # ======================================
                # ERROR
                # ======================================
                case PageType.ERROR:
                    ScreenshotService.save(
                        page,
                        application_id,
                        f"{screenshot_counter:03d}_error_page.png",
                    )
                    raise Exception(
                        "Error page detected: Job may no longer be available."
                    )

                # ======================================
                # SUCCESS
                # ======================================
                case PageType.SUCCESS:
                    AutomationLogService.log(
                        application_id,
                        "Application submitted successfully!"
                    )
                    ScreenshotService.save(
                        page,
                        application_id,
                        f"{screenshot_counter:03d}_success.png",
                    )
                    return  # Exit the loop — we're done

                # ======================================
                # LOGIN
                # ======================================
                case PageType.LOGIN:
                    self._handle_login(
                        page,
                        application_id,
                    )
                    continue

                # ======================================
                # APPLY (landing with apply button)
                # ======================================
                case PageType.APPLY:
                    self._handle_apply(
                        page,
                        application_id,
                        screenshot_counter,
                    )
                    screenshot_counter += 1
                    # Reset counters
                    loading_count = 0
                    unknown_count = 0
                    continue

                # ======================================
                # FORM
                # ======================================
                case PageType.FORM:
                    resume_uploaded = self._handle_form(
                        page,
                        application_id,
                        resume,
                        screenshot_counter,
                        resume_uploaded,
                    )
                    screenshot_counter += 1
                    loading_count = 0
                    unknown_count = 0
                    continue

                # ======================================
                # REVIEW
                # ======================================
                case PageType.REVIEW:
                    self._handle_review(
                        page,
                        application_id,
                        screenshot_counter,
                    )
                    screenshot_counter += 1
                    loading_count = 0
                    unknown_count = 0
                    continue

                # ======================================
                # LANDING (job description page)
                # ======================================
                case PageType.LANDING:
                    self._handle_landing(
                        page,
                        application_id,
                        screenshot_counter,
                    )
                    screenshot_counter += 1
                    loading_count = 0
                    unknown_count = 0
                    continue

                # ======================================
                # WAITING_USER
                # ======================================
                case PageType.WAITING_USER:
                    AutomationLogService.log(
                        application_id,
                        "Waiting for user input: ambiguous fields or complex questions require human action."
                    )
                    raise Exception("Automation paused: waiting for user input on complex fields.")

                # ======================================
                # UNKNOWN
                # ======================================
                case PageType.UNKNOWN:
                    unknown_count += 1
                    if unknown_count > self.MAX_UNKNOWN_RETRIES:
                        ScreenshotService.save(
                            page,
                            application_id,
                            f"{screenshot_counter:03d}_unknown_stuck.png",
                        )
                        raise Exception(
                            "Automation stuck: Unable to classify page after multiple attempts."
                        )
                    AutomationLogService.log(
                        application_id,
                        f"Unknown page state. Retrying... ({unknown_count}/{self.MAX_UNKNOWN_RETRIES})"
                    )
                    page.wait_for_timeout(3000)
                    continue

        # If we exhaust MAX_STEPS
        raise Exception(
            f"Automation exceeded maximum steps ({self.MAX_STEPS}). Possible infinite loop."
        )

    # ==========================================================================
    # PAGE TYPE HANDLERS
    # ==========================================================================

    def _handle_login(self, page, application_id: str):
        """
        Wait for the user to complete authentication.
        Poll until the login page is no longer detected.
        """
        AutomationLogService.log(
            application_id,
            "Login required. Waiting for user authentication..."
        )

        max_login_wait = 120  # seconds
        elapsed = 0

        while PageDetector.detect(page) == PageType.LOGIN:
            if elapsed >= max_login_wait:
                raise Exception(
                    "Login timeout: User did not authenticate within 2 minutes."
                )
            time.sleep(self.LOGIN_POLL_SECONDS)
            elapsed += self.LOGIN_POLL_SECONDS
            app_logger.info(
                f"Waiting for login... ({elapsed}s / {max_login_wait}s)"
            )

        AutomationLogService.log(
            application_id,
            "User authenticated. Resuming automation."
        )

    # --------------------------------------------------

    def _handle_apply(self, page, application_id: str, screenshot_counter: int):
        """Click the Apply button and wait for the next page."""
        AutomationLogService.log(
            application_id,
            "Apply button detected. Clicking..."
        )

        success = ApplyAction.execute(page, application_id)

        if success:
            AutomationLogService.log(
                application_id,
                "Apply button clicked successfully."
            )
            ScreenshotService.save(
                page,
                application_id,
                f"{screenshot_counter:03d}_after_apply.png",
            )
        else:
            AutomationLogService.log(
                application_id,
                "Apply button could not be clicked."
            )
            # Wait and try again on next iteration
            page.wait_for_timeout(2000)

    # --------------------------------------------------

    def _handle_landing(self, page, application_id: str, screenshot_counter: int):
        """
        Handle a job listing / landing page.
        Try to find and click the Apply button.
        If not found, this may be a direct-apply URL.
        """
        AutomationLogService.log(
            application_id,
            "Landing page detected. Looking for Apply button..."
        )

        success = ApplyAction.execute(page, application_id)

        if success:
            AutomationLogService.log(
                application_id,
                "Apply button clicked from landing page."
            )
            ScreenshotService.save(
                page,
                application_id,
                f"{screenshot_counter:03d}_after_landing_apply.png",
            )
        else:
            AutomationLogService.log(
                application_id,
                "No Apply button found on landing page. Page may auto-redirect."
            )
            page.wait_for_timeout(3000)

    # --------------------------------------------------

    # Maximum retries for filling remaining fields before
    # giving up on a single form page.
    MAX_FORM_RETRIES = 3

    def _handle_form(
        self,
        page,
        application_id: str,
        resume,
        screenshot_counter: int,
        resume_uploaded: bool = False,
    ) -> bool:
        """
        Parse form fields, match to resume data,
        fill fields, upload resume, and navigate.

        Returns the updated resume_uploaded flag so the
        state machine can track it across iterations.
        """
        AutomationLogService.log(
            application_id,
            "Form page detected. Scanning fields..."
        )

        # ------------------------------------------
        # Upload resume ONCE per application
        # ------------------------------------------
        if not resume_uploaded and resume and resume.file_path:
            uploaded = UploadEngine.process(page, resume.file_path)
            if uploaded:
                resume_uploaded = True
                AutomationLogService.log(
                    application_id,
                    "Resume uploaded."
                )

        # ------------------------------------------
        # Fill → Validate → Retry loop
        # ------------------------------------------
        for retry in range(self.MAX_FORM_RETRIES):
            if retry > 0:
                AutomationLogService.log(
                    application_id,
                    f"Retrying form fill (attempt {retry + 1}/{self.MAX_FORM_RETRIES})..."
                )

            # ------------------------------------------
            # Parse visible form fields
            # ------------------------------------------
            fields = FieldParser.parse(page)
            AutomationLogService.log(
                application_id,
                f"Found {len(fields)} form fields."
            )

            # ------------------------------------------
            # Match and fill each field
            # ------------------------------------------
            filled_count = 0
            skipped_count = 0

            for field in fields:
                answer = AnswerMatcher.match(
                    field,
                    resume.resume_json,
                    resume.file_path,
                )

                if answer is not None:
                    FieldFiller.fill(field, answer)
                    filled_count += 1
                    AutomationLogService.log(
                        application_id,
                        f"Filled field '{field.label}' (name: '{field.name}', type: '{field.field_type.value}') with: {answer}"
                    )
                else:
                    skipped_count += 1
                    reason = "No matching value found in resume profile"
                    if not field.label and not field.placeholder and not field.name:
                        reason = "Field has no visible label, placeholder, or name attribute"
                    elif field.field_type == FieldType.UNKNOWN:
                        reason = "Field type is unknown/unsupported"
                    AutomationLogService.log(
                        application_id,
                        f"Skipped field '{field.label}' (name: '{field.name}', type: '{field.field_type.value}'). Reason: {reason}"
                    )

            AutomationLogService.log(
                application_id,
                f"Fields filled: {filled_count}, Skipped: {skipped_count}"
            )

            # ------------------------------------------
            # Screenshot before navigation
            # ------------------------------------------
            ScreenshotService.save(
                page,
                application_id,
                f"{screenshot_counter:03d}_form_filled.png",
            )

            # ------------------------------------------
            # Navigate to next page
            # ------------------------------------------
            AutomationLogService.log(application_id, "Navigating to next step...")

            result = NavigationEngine.process(page, application_id)

            AutomationLogService.log(
                application_id,
                f"Navigation result: {result.value}"
            )

            if result != NavigationResult.NO_ACTION:
                # Navigation succeeded (NEXT, SUBMIT, REVIEW, etc.)
                return resume_uploaded

            # Navigation was blocked — required fields still incomplete.
            # Wait briefly then retry filling the remaining fields.
            AutomationLogService.log(
                application_id,
                "Navigation blocked: required fields still incomplete. Will retry filling..."
            )
            page.wait_for_timeout(2000)

        # Exhausted retries — return to state machine for re-detection
        AutomationLogService.log(
            application_id,
            f"Form fill retries exhausted ({self.MAX_FORM_RETRIES}). Returning to state machine."
        )
        return resume_uploaded

    # --------------------------------------------------

    def _handle_review(self, page, application_id: str, screenshot_counter: int):
        """
        Handle the review/preview page.
        Take a screenshot and attempt to submit.
        """
        AutomationLogService.log(
            application_id,
            "Review page detected. Capturing screenshot..."
        )

        ScreenshotService.save(
            page,
            application_id,
            f"{screenshot_counter:03d}_review.png",
        )

        AutomationLogService.log(
            application_id,
            "Attempting to submit application..."
        )

        result = NavigationEngine.process(page, application_id)

        AutomationLogService.log(
            application_id,
            f"Submit navigation result: {result.value}"
        )

    # ==========================================================================
    # UTILITIES
    # ==========================================================================

    def _wait_for_network(self, application_id: str):
        """Block until network connectivity is restored."""
        if NetworkService.is_online():
            return

        AutomationLogService.log(
            application_id,
            "Internet connection lost. Waiting..."
        )

        while not NetworkService.is_online():
            time.sleep(3)

        AutomationLogService.log(
            application_id,
            "Internet connection restored."
        )