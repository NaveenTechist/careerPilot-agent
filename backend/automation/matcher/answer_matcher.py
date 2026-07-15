"""
Answer Matcher.

Maps detected form fields
to resume/application values.
"""

from automation.models.field import Field
from automation.models.field_type import FieldType


class AnswerMatcher:

    @staticmethod
    def match(
        field,
        resume_json,
        resume_path,
    ):
        
        data = resume_json
        label = (
            field.label
            or field.placeholder
            or field.name
        ).lower()

        # -----------------------------
        # Name
        # -----------------------------

        if "first" in label and "name" in label:
            return resume.get("first_name")

        if "last" in label and "name" in label:
            return resume.get("last_name")

        if label == "name":
            return resume.get("name")

        # -----------------------------
        # Contact
        # -----------------------------
        if "email" in label:
            return resume.get("email")
        if "phone" in label:
            return resume.get("phone")
        if "mobile" in label:
            return resume.get("phone")
        # -----------------------------
        # Location
        # -----------------------------
        if "city" in label:
            return resume.get("city")
        if "country" in label:
            return resume.get("country")
        if "state" in label:
            return resume.get("state")
        # -----------------------------
        # Links
        # -----------------------------
        if "linkedin" in label:
            return resume.get("linkedin")
        if "github" in label:
            return resume.get("github")
        if "portfolio" in label:
            return resume.get("portfolio")
        # -----------------------------
        # Resume
        # -----------------------------
        if field.field_type == FieldType.FILE:
            return resume.file_path
        return None