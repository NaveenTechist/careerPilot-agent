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

    ]

    @classmethod
    def process(
        cls,
        page,
    ):

        if SuccessDetector.detect(page):

            return NavigationResult.SUCCESS

        for text, result in cls.BUTTONS:

            button = page.get_by_role(

                "button",

                name=text,

                exact=False,

            )

            if button.count() > 0:

                BrowserActions.click(

                    button.first

                )

                BrowserActions.wait(page)

                return result

        return NavigationResult.NO_ACTION