"""
Result returned by every extraction strategy.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class StrategyResult:
    success: bool
    strategy: str
    content: str | None = None
    error: str | None = None
