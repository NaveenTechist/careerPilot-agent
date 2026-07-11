"""
Automation Context.

Contains everything required
to complete one application.
"""

from dataclasses import dataclass


@dataclass
class AutomationContext:

    application: object

    resume: object

    job: object

    resume_path: str