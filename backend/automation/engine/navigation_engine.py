from automation.detector.success_detector import SuccessDetector
from automation.browser.browser_actions import BrowserActions
from automation.navigation.navigation_result import NavigationResult


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
    def process(
        cls,
        page,
    ):

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
                    BrowserActions.click(button)
                    BrowserActions.wait(page)
                    return result
        return NavigationResult.NO_ACTION