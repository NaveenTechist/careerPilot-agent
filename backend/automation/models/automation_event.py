from pydantic import BaseModel
from automation.models.automation_state import AutomationState


from dataclasses import dataclass


@dataclass
class AutomationEvent:

    application_id: str
    progress: int
    step: str
    message: str
    completed: bool = False