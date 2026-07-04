"""
Match Result Model.

Represents AI analysis between

ResumeProfile

and

JobProfile.
"""

from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    # Overall Score
    score: int = Field(
        ge=0,
        le=100,
    )
    # Matching
    matched_skills: list[str] = Field(
        default_factory=list
    )
    missing_skills: list[str] = Field(
        default_factory=list
    )
    # AI Explanation
    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )
    recommendation: str
    should_apply: bool