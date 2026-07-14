from automation.navigation.navigation_result import NavigationResult
from automation.detector.success_detector import SuccessDetector
from automation.browser.browser_actions import BrowserActions


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
            for keyword in cls.BUTTONS:
                if keyword.lower() in label.lower():
                    BrowserActions.click(button)
                    BrowserActions.wait(page)
                    return NavigationResult.NEXT
        return NavigationResult.NOT_FOUND