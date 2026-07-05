"""
Match Entity.

Stores the AI matching result between
a ResumeProfile and a JobProfile.

This becomes the single source of truth
before browser automation starts.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from database.base import Base


class MatchStatus(str, Enum):
    """
    Lifecycle of a match.
    """

    PENDING = "PENDING"
    PROCEEDED = "PROCEEDED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class MatchEntity(Base):

    __tablename__ = "match_results"

    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # --------------------------------------------------
    # References
    # --------------------------------------------------

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    # --------------------------------------------------
    # Match Summary
    # --------------------------------------------------

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    recommendation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    should_apply: Mapped[bool]

    status: Mapped[MatchStatus] = mapped_column(
        SqlEnum(MatchStatus),
        default=MatchStatus.PENDING,
        nullable=False,
    )

    # --------------------------------------------------
    # Complete AI Response
    # --------------------------------------------------

    match_json: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # --------------------------------------------------
    # Audit Fields
    # --------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )