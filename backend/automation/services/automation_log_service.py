"""
Automation Log Service.

Responsible only for:

- Writing automation logs
- Console output
- Future DB integration
"""

from pathlib import Path
from datetime import datetime


class AutomationLogService:

    ROOT = Path("automation/logs")

    @classmethod
    def log(
        cls,
        application_id: str,
        message: str,
    ):

        cls.ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

        logfile = cls.ROOT / f"{application_id}.log"

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            logfile,
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                f"[{timestamp}] {message}\n"
            )

        print(message)