from dataclasses import dataclass

from playwright.sync_api import Locator

from automation.models.field_type import FieldType


@dataclass(slots=True)
class Field:

    locator: Locator
    tag: str
    field_type: FieldType
    label: str
    name: str
    placeholder: str
    required: bool
    options: list[str] | None = None