from automation.strategies.strategy import Strategy

from automation.browser.browser_actions import BrowserActions


class LinkedInStrategy(Strategy):

    def run(

        self,

        page,

        application,

    ):

        BrowserActions.open_url(

            page,

            application.job.application_url,

        )

        print(

            "LinkedIn Strategy"

        )