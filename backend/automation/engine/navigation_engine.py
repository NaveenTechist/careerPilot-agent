from automation.detector.success_detector import SuccessDetector
from automation.browser.browser_actions import BrowserActions
from automation.navigation.navigation_result import NavigationResult
from core.logger import app_logger


class NavigationEngine:

    BUTTONS = [
        ("Submit", NavigationResult.SUBMIT),
        ("Review", NavigationResult.REVIEW),
        ("Next", NavigationResult.NEXT),
        ("Continue", NavigationResult.NEXT),
        ("Save and Continue", NavigationResult.NEXT),
        "Submit",
        "Apply",
        "Apply Now",
        "Finish",
        "Complete",
        "Continue Application",
        "Review Application",
        "Proceed",
    ]

    @classmethod
    def _verify_page_validity(cls, page) -> tuple[bool, str | None]:
        """
        Verifies that all required fields are completed and no visible
        validation error messages exist on the page.
        """
        from automation.parser.field_parser import FieldParser
        from automation.models.field_type import FieldType

        # 1. Verify required fields
        fields = FieldParser.parse(page)
        for field in fields:
            if field.required:
                completed = False
                try:
                    locator = field.locator
                    if field.field_type == FieldType.RADIO:
                        # For radio groups, at least one option must be checked
                        name = field.name
                        if name:
                            radios = page.locator(f"input[type='radio'][name='{name}']")
                            r_count = radios.count()
                            for r_idx in range(r_count):
                                if radios.nth(r_idx).is_checked():
                                    completed = True
                                    break
                        else:
                            completed = locator.is_checked()
                    elif field.field_type == FieldType.CHECKBOX:
                        completed = locator.is_checked()
                    elif field.field_type == FieldType.SELECT:
                        val = locator.evaluate("e => e.value")
                        completed = val is not None and len(str(val).strip()) > 0
                    else:
                        val = locator.evaluate("e => e.value")
                        completed = val is not None and len(str(val).strip()) > 0
                except Exception:
                    pass

                if not completed:
                    return False, f"Required field '{field.label}' (name: '{field.name}') is not completed."

        # 2. Check for visible validation errors
        error_selectors = [
            ".error:visible",
            ".invalid:visible",
            ".alert-danger:visible",
            "[aria-invalid='true']:visible",
            "[class*='error' i]:visible",
            "[class*='invalid' i]:visible",
            "[id*='error' i]:visible",
            "[id*='invalid' i]:visible",
        ]
        for sel in error_selectors:
            try:
                loc = page.locator(sel)
                count = loc.count()
                for idx in range(count):
                    el = loc.nth(idx)
                    text = (el.inner_text() or "").strip()
                    # Skip empty divs or containers holding input controls
                    if text and len(text) > 3 and el.locator("input, select, textarea").count() == 0:
                        return False, f"Visible validation error message: '{text}'"
            except Exception:
                continue

        return True, None

    @classmethod
    def process(
        cls,
        page,
        application_id: str = None,
    ):

        from automation.detector.modal_detector import ModalDetector
        modal_status = ModalDetector.detect_and_handle(page, application_id)
        if modal_status == "WAITING_USER":
            return NavigationResult.WAITING_USER

        if SuccessDetector.detect(page):
            return NavigationResult.SUCCESS

        buttons = page.locator(
            "button,input[type='submit'],a[role='button']"
        )

        count = buttons.count()

        for i in range(count):
            button = buttons.nth(i)
            try:
                label = button.inner_text().strip()
            except:
                continue
            for item in cls.BUTTONS:
                if isinstance(item, tuple):
                    keyword, result = item
                else:
                    keyword = item
                    # fallback mapping
                    if "submit" in keyword.lower():
                        result = NavigationResult.SUBMIT
                    elif "review" in keyword.lower():
                        result = NavigationResult.REVIEW
                    else:
                        result = NavigationResult.NEXT
                
                if keyword.lower() in label.lower():
                    # Before executing submit/review/next progress actions, verify page completeness and validity
                    if result in (NavigationResult.SUBMIT, NavigationResult.REVIEW, NavigationResult.NEXT):
                        is_valid, reason = cls._verify_page_validity(page)
                        if not is_valid:
                            from automation.services.automation_log_service import AutomationLogService
                            msg = f"Navigation action '{label}' ({result.value}) blocked: {reason}"
                            app_logger.warning(msg)
                            if application_id:
                                AutomationLogService.log(application_id, msg)
                            return NavigationResult.NO_ACTION

                    BrowserActions.click(button)
                    BrowserActions.wait(page)
                    return result
        return NavigationResult.NO_ACTION