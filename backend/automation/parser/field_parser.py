from playwright.sync_api import Page

from automation.models.field import Field
from automation.models.field_type import FieldType

from automation.parser.label_parser import LabelParser


class FieldParser:

    SELECTOR = """
input,
textarea,
select
"""

    @classmethod
    def parse(
        cls,
        page: Page,
    ) -> list[Field]:

        fields = []

        elements = page.locator(
            cls.SELECTOR
        )

        count = elements.count()

        for i in range(count):

            locator = elements.nth(i)

            try:

                if not locator.is_visible():

                    continue

                tag = locator.evaluate(
                    "e=>e.tagName.toLowerCase()"
                )

                input_type = (
                    locator.get_attribute("type")
                    or ""
                ).lower()
                if tag == "textarea":
                    field_type = FieldType.TEXTAREA
                elif tag == "select":
                    field_type = FieldType.SELECT
                elif input_type == "radio":
                    field_type = FieldType.RADIO
                elif input_type == "checkbox":
                    field_type = FieldType.CHECKBOX
                elif input_type == "file":
                    field_type = FieldType.FILE
                elif input_type == "email":
                    field_type = FieldType.EMAIL
                elif input_type == "tel":
                    field_type = FieldType.PHONE
                elif input_type == "number":
                    field_type = FieldType.NUMBER
                elif input_type == "date":
                    field_type = FieldType.DATE
                else:
                    field_type = FieldType.TEXT
                fields.append(
                    Field(
                        locator=locator,
                        tag=tag,
                        field_type=field_type,
                        label=LabelParser.parse(locator),
                        name=locator.get_attribute("name") or "",
                        placeholder=locator.get_attribute("placeholder") or "",
                        required=locator.get_attribute("required") is not None,
                    )
                )
            except Exception:
                continue
        return fields