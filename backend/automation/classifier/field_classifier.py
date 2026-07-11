"""
Universal Field Classifier.
"""

from automation.models.form_field import FormField
from automation.classifier.field_type import FieldType
from automation.utils.text_utils import TextUtils


class FieldClassifier:

    @staticmethod
    def classify(

        field: FormField,

    ) -> FieldType:

        text = " ".join(

            [

                field.label,

                field.name,

                field.placeholder,

            ]

        )

        text = TextUtils.normalize(text)

        # -------------------------
        # Resume
        # -------------------------

        if field.input_type == "file":

            return FieldType.RESUME_UPLOAD

        # -------------------------
        # Email
        # -------------------------

        if "email" in text:

            return FieldType.EMAIL

        # -------------------------
        # Phone
        # -------------------------

        if "phone" in text:

            return FieldType.PHONE

        if "mobile" in text:

            return FieldType.PHONE

        # -------------------------
        # Name
        # -------------------------

        if "first name" in text:

            return FieldType.FIRST_NAME

        if "last name" in text:

            return FieldType.LAST_NAME

        if "full name" in text:

            return FieldType.FULL_NAME

        if text == "name":

            return FieldType.FULL_NAME

        # -------------------------
        # Links
        # -------------------------

        if "linkedin" in text:

            return FieldType.LINKEDIN

        if "github" in text:

            return FieldType.GITHUB

        if "portfolio" in text:

            return FieldType.PORTFOLIO

        # -------------------------
        # Salary
        # -------------------------

        if "salary" in text:

            return FieldType.SALARY

        if "ctc" in text:

            return FieldType.SALARY

        # -------------------------
        # Notice
        # -------------------------

        if "notice" in text:

            return FieldType.NOTICE_PERIOD

        # -------------------------
        # Sponsorship
        # -------------------------

        if "sponsorship" in text:

            return FieldType.SPONSORSHIP

        if "visa" in text:

            return FieldType.WORK_AUTHORIZATION

        # -------------------------
        # Disability
        # -------------------------

        if "disability" in text:

            return FieldType.DISABILITY

        if "veteran" in text:

            return FieldType.VETERAN

        # -------------------------
        # Controls
        # -------------------------

        if field.tag == "textarea":

            return FieldType.TEXTAREA

        if field.tag == "select":

            return FieldType.DROPDOWN

        if field.input_type == "checkbox":

            return FieldType.CHECKBOX

        if field.input_type == "radio":

            return FieldType.RADIO

        return FieldType.UNKNOWN