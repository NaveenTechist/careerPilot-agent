"""
Maps classified fields
to candidate values.
"""

from automation.classifier.field_type import FieldType


class FormMapper:

    @staticmethod
    def value(

        field_type,

        context,

    ):

        resume = context.resume

        if field_type == FieldType.EMAIL:

            return resume.email

        if field_type == FieldType.PHONE:

            return resume.phone

        if field_type == FieldType.FULL_NAME:

            return resume.name

        if field_type == FieldType.FIRST_NAME:

            return resume.name.split()[0]

        if field_type == FieldType.LAST_NAME:

            names = resume.name.split()

            return names[-1]

        if field_type == FieldType.LINKEDIN:

            return resume.linkedin

        if field_type == FieldType.GITHUB:

            return resume.github

        return None