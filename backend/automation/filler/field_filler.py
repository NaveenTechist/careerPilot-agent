"""
Field Filler.

Responsible for filling any supported form field.
"""

from automation.browser.browser_actions import BrowserActions
from automation.models.field_type import FieldType
from core.logger import app_logger


class FieldFiller:
    @staticmethod
    def fill(field, value):
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

                    try:
                        locator.select_option(label=str(value))
                    except Exception:
                        try:
                            locator.select_option(value=str(value))
                        except Exception:
                            # Substring match fallback for select options
                            options = locator.locator("option")
                            count = options.count()
                            matched = False
                            for idx in range(count):
                                opt = options.nth(idx)
                                text = (opt.inner_text() or "").lower()
                                if str(value).lower() in text or text in str(value).lower():
                                    locator.select_option(index=idx)
                                    matched = True
                                    break
                            if not matched:
                                raise

                case FieldType.CHECKBOX:

                    if bool(value):
                        try:
                            locator.check(timeout=2000)
                        except Exception:
                            try:
                                locator.click(force=True, timeout=1000)
                            except Exception:
                                locator.evaluate("el => el.checked = true")
                                locator.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
                    else:
                        try:
                            locator.uncheck(timeout=2000)
                        except Exception:
                            try:
                                locator.click(force=True, timeout=1000)
                            except Exception:
                                locator.evaluate("el => el.checked = false")
                                locator.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")

                case FieldType.RADIO:

                    # Only check the radio option if the matcher returned True for it
                    if bool(value):
                        try:
                            locator.check(timeout=2000)
                        except Exception:
                            try:
                                locator.click(force=True, timeout=1000)
                            except Exception:
                                locator.evaluate("el => el.checked = true")
                                locator.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")

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