from automation.browser.browser_manager import BrowserManager

from automation.browser.browser_actions import BrowserActions

browser = BrowserManager()

page = browser.launch()

BrowserActions.open_url(

    page,

    "https://github.com"

)

BrowserActions.wait(

    page,

    2,

)

BrowserActions.scroll_bottom(

    page,

)

BrowserActions.wait(

    page,

    2,

)

browser.close()