from automation.browser.browser_actions import BrowserActions


class FieldFiller:

    @staticmethod
    def fill(
        page,
        field,
        value,
    ):

        if value is None:
            return

        locator = page.locator(
            field.selector
        )

        try:

            if field.tag == "textarea":

                BrowserActions.fill(
                    locator,
                    value,
                )

            elif field.tag == "select":

                locator.select_option(
                    label=str(value)
                )

            elif field.input_type == "checkbox":

                if bool(value):
                    locator.check()

            elif field.input_type == "radio":

                locator.check()

            elif field.input_type == "file":

                BrowserActions.upload(
                    locator,
                    value,
                )

            else:

                BrowserActions.fill(
                    locator,
                    value,
                )

        except Exception:

            pass