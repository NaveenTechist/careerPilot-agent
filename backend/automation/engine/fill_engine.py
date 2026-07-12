class FillEngine:

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

        if field.tag == "textarea":

            locator.fill(str(value))

        elif field.tag == "select":

            locator.select_option(
                label=str(value)
            )

        elif field.input_type == "checkbox":

            locator.check()

        elif field.input_type == "radio":

            locator.check()

        elif field.input_type == "file":

            locator.set_input_files(
                value
            )

        else:

            locator.fill(
                str(value)
            )