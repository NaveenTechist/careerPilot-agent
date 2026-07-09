from automation.browser.browser_manager import BrowserManager
from automation.detector.form_detector import FormDetector

browser = BrowserManager()
page = browser.launch()
page.goto(
    "https://www.w3schools.com/html/html_forms.asp"
)
fields = FormDetector.scan(page)
print()
print("=" * 80)
print("FIELDS FOUND")
print("=" * 80)
for field in fields:
    print(field)
print("=" * 80)
input()
browser.close()