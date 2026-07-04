"""
Centralized application logger.

Every module imports this logger instead of creating its own logger.

Reason:
--------
A single logging configuration keeps logs consistent across the
entire application and makes it easy to later integrate with
production log systems like Grafana, ELK or CloudWatch.
"""

from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    backtrace=True,
    diagnose=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)

app_logger = logger
