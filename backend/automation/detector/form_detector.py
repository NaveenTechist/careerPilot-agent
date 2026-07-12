"""
Form Detector.

Scans every form element
from any webpage.

Returns List[FormField]
"""

from playwright.sync_api import Page
from automation.models.form_field import FormField

class FormDetector:
    @staticmethod
    def scan(
        page: Page,
    ) -> list[FormField]:
        fields = []
        elements = page.locator(
            "input, textarea, select"
        )
        total = elements.count()
        for i in range(total):
            element = elements.nth(i)
            try:
                tag = element.evaluate(
                    "e => e.tagName.toLowerCase()"
                )
                input_type = element.get_attribute("type") or ""
                name = element.get_attribute("name") or ""
                placeholder = element.get_attribute("placeholder") or ""
                element_id = element.get_attribute("id") or ""
                required = (
                    element.get_attribute("required")
                    is not None
                )
                label = ""
                if element_id:
                    label_locator = page.locator(
                        f"label[for='{element_id}']"
                    )
                    if label_locator.count() > 0:
                        label = label_locator.first.inner_text()
                field = FormField(
                    selector=f"input:nth-of-type({i+1})",
                    tag=tag,
                    input_type=input_type,
                    name=name,
                    placeholder=placeholder,
                    element_id=element_id,
                    label=label,
                )
                field.required = required
                fields.append(field)
            except Exception:
                continue