"""
Field Filler.

Responsible for filling any supported form field.
"""

from automation.browser.browser_actions import BrowserActions
from automation.models.field_type import FieldType
from core.logger import app_logger


class FieldFiller:

    @staticmethod
    def fill(
        field,
        value,
    ):

        if value is None:
            return

        locator = field.locator

        try:

            match field.field_type:

                case FieldType.TEXT:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

                case FieldType.EMAIL:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

                case FieldType.PHONE:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

                case FieldType.NUMBER:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

                case FieldType.TEXTAREA:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

                case FieldType.SELECT:

                    locator.select_option(
                        label=str(value),
                    )

                case FieldType.CHECKBOX:

                    if bool(value):

                        locator.check()

                case FieldType.RADIO:

                    locator.check()

                case FieldType.FILE:

                    BrowserActions.upload(
                        locator,
                        str(value),
                    )

                case FieldType.DATE:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

                case _:

                    BrowserActions.fill(
                        locator,
                        str(value),
                    )

        except Exception as e:

            app_logger.exception(
                f"Failed to fill '{field.label}': {e}"
            )