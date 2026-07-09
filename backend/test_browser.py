from automation.browser.browser_manager import BrowserManager

browser = BrowserManager()

page = browser.launch()

page.goto(
    "https://google.com"
)

input("Browser Opened. Press Enter...")

browser.close()