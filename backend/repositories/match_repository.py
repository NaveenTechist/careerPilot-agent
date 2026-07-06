"""
Match Repository.

Responsible only for database operations.

Responsibilities
----------------
- Save Match
- Get Latest Match
- Get Match By ID
- Update Status
"""

from uuid import UUID
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.match_result import MatchResult
from models.db.match_entity import MatchEntity
from models.db.match_entity import MatchStatus
from core.logger import app_logger


class MatchRepository:
    # ---------------------------------------------

    def save(
        self,
        resume_id: UUID,
        job_id: UUID,
        result: MatchResult,
    ) -> MatchEntity:
        app_logger.info("Saving match result.")
        db: Session = SessionLocal()
        try:
            entity = MatchEntity(
                resume_id=resume_id,
                job_id=job_id,
                score=result.score,
                recommendation=result.recommendation,
                should_apply=result.should_apply,
                status=MatchStatus.PENDING,
                match_json=result.model_dump(),
            )
            db.add(entity)
            db.commit()
            db.refresh(entity)
            app_logger.success(f"Match saved successfully. id={entity.id}")
            return entity
        except Exception:
            db.rollback()
            app_logger.exception("Failed to save match.")
            raise
        finally:
            db.close()

    # ---------------------------------------------

    def get_latest(self):
        db = SessionLocal()
        try:
            return db.query(MatchEntity).order_by(MatchEntity.created_at.desc()).first()
        finally:
            db.close()

    # ---------------------------------------------
    def get_by_id(
        self,
        match_id: UUID,
    ):
        db = SessionLocal()
        try:
            return db.query(MatchEntity).filter(MatchEntity.id == match_id).first()
        finally:
            db.close()

    # ---------------------------------------------

    def update_status(
        self,
        match_id: UUID,
        status: MatchStatus,
    ):
        db = SessionLocal()
        try:
            entity = db.query(MatchEntity).filter(MatchEntity.id == match_id).first()
            if entity is None:
                return None
            entity.status = status
            db.commit()
            db.refresh(entity)
            app_logger.success(f"Match status updated to {status}")
            return entity
        except Exception:
            db.rollback()
            app_logger.exception("Unable to update match status.")
            raise
        finally:
            db.close()

    # ---------------------------------------------
    def delete_all(self):
        db = SessionLocal()
        try:
            db.query(MatchEntity).delete()
            db.commit()
            app_logger.success("All matches deleted.")
        finally:
            db.close()
