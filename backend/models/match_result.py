"""
Match Result Model.

Represents the comparison between
ResumeProfile and JobProfile.
"""

from pydantic import BaseModel


class MatchResult(BaseModel):
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str
    should_apply: bool
