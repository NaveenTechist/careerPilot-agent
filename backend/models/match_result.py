"""
Match Result Model.

Represents the AI analysis between a
ResumeProfile and a JobProfile.

This model is returned by the
MatchingAgent and stored in the database.
"""

from pydantic import BaseModel
from pydantic import Field


class MatchResult(BaseModel):
    """
    Final AI matching result.
    """

    # --------------------------------------------------
    # Overall Match Score
    # --------------------------------------------------

    score: int = Field(
        ge=0,
        le=100,
        description="Overall compatibility score.",
    )

    overall_level: str = Field(
        description="Excellent, Good, Moderate or Poor",
    )

    should_apply: bool

    # --------------------------------------------------
    # Skill Analysis
    # --------------------------------------------------

    matched_skills: list[str] = Field(
        default_factory=list,
    )

    missing_skills: list[str] = Field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Strength Analysis
    # --------------------------------------------------

    strengths: list[str] = Field(
        default_factory=list,
    )

    weaknesses: list[str] = Field(
        default_factory=list,
    )

    # --------------------------------------------------
    # AI Recommendation
    # --------------------------------------------------

    recommendation: str

    next_steps: list[str] = Field(
        default_factory=list,
    )