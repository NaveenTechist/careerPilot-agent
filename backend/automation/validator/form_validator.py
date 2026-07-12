class FormValidator:

    @staticmethod
    def validate(
        page,
    ):
        errors = page.locator(
            ".error,.invalid,.field-error"
        )
        return errors.count() == 0