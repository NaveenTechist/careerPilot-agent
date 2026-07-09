from automation.browser.browser_manager import BrowserManager
from automation.services.screenshot_service import ScreenshotService

browser = BrowserManager()

page = browser.launch()

page.goto(
    "https://github.com"
)

path = ScreenshotService.save(
    page=page,
    application_id="demo-application",
    filename="001_home.png",
)

print(path)

input("Press Enter...")

browser.close()