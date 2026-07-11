from dataclasses import dataclass
from datetime import datetime


@dataclass
class AutomationEvent:

    application_id: str
    type: str
    step: str
    message: str
    progress: int
    timestamp: datetime