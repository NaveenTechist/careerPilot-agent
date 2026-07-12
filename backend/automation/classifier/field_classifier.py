from enum import Enum

from automation.models.form_field import FormField


class FieldType(str, Enum):

    FIRST_NAME = "FIRST_NAE"
    LAST_NAME = "LAST_NAME"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    CITY = "CITY"
    STATE = "STATE"
    COUNTRY = "COUNTRY"
    ZIP = "ZIP"
    ADDRESS = "ADDRESS"
    LINKEDIN = "LINKEDIN"
    GITHUB = "GITHUB"
    PORTFOLIO = "PORTFOLIO"
    RESUME = "RESUME"
    COVER_LETTER = "COVER_LETTER"
    NOTICE_PERIOD = "NOTICE_PERIOD"
    EXPERIENCE = "EXPERIENCE"
    CURRENT_CTC = "CURRENT_CTC"
    EXPECTED_CTC = "EXPECTED_CTC"
    SPONSORSHIP = "SPONSORSHIP"
    WORK_AUTHORIZATION = "WORK_AUTHORIZATION"
    DISABILITY = "DISABILITY"
    GENDER = "GENDER"
    DOB = "DOB"
    UNKNOWN = "UNKNOWN"


class FieldClassifier:

    MAP = {
        "firstname": FieldType.FIRST_NAME,
        "first name": FieldType.FIRST_NAME,
        "fname": FieldType.FIRST_NAME,
        "lastname": FieldType.LAST_NAME,
        "surname": FieldType.LAST_NAME,
        "email": FieldType.EMAIL,
        "mail": FieldType.EMAIL,
        "phone": FieldType.PHONE,
        "mobile": FieldType.PHONE,
        "linkedin": FieldType.LINKEDIN,
        "github": FieldType.GITHUB,
        "portfolio": FieldType.PORTFOLIO,
        "resume": FieldType.RESUME,
        "cv": FieldType.RESUME,
        "notice": FieldType.NOTICE_PERIOD,
        "salary": FieldType.EXPECTED_CTC,
        "ctc": FieldType.CURRENT_CTC,
        "sponsorship": FieldType.SPONSORSHIP,
        "work authorization": FieldType.WORK_AUTHORIZATION,
        "disability": FieldType.DISABILITY,

    }

    @classmethod
    def classify(
        cls,
        field: FormField,
    ):
        text = " ".join([
            field.name or "",
            field.label or "",
            field.placeholder or "",
        ]).lower()
        for key, value in cls.MAP.items():
            if key in text:
                return value
        return FieldType.UNKNOWN    