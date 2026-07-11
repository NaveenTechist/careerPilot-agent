"""
Automation Log Service.

Responsible only for writing
automation logs.
"""

from pathlib import Path
from datetime import datetime

from core.logger import app_logger


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

        line = f"[{timestamp}] {message}\n"

        with logfile.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(line)

        app_logger.info(message)

    # --------------------------------------------------

    @classmethod
    def clear(
        cls,
        application_id: str,
    ):

        logfile = cls.ROOT / f"{application_id}.log"

        if logfile.exists():

            logfile.unlink()

    # --------------------------------------------------

    @classmethod
    def read(
        cls,
        application_id: str,
    ):

        logfile = cls.ROOT / f"{application_id}.log"

        if not logfile.exists():

            return []

        return logfile.read_text(
            encoding="utf-8",
        ).splitlines()