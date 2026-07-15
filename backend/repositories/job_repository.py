"""
Job Repository.

Responsible only for database operations.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.job_profile import JobProfile
from models.db.job_entity import JobEntity
from core.logger import app_logger
import uuid
from services.hashing_service import HashingService


class JobRepository:
    def save(
        self,
        profile: JobProfile,
        url_hash: str | None = None,
    ) -> JobEntity:

        if url_hash is None:
            url_hash = HashingService.text_sha256(profile.application_url or "")
        app_logger.info("Saving job profile.")
        db: Session = SessionLocal()
        try:
            entity = JobEntity(
                company=profile.company,
                job_title=profile.job_title,
                application_url=profile.application_url,
                url_hash=url_hash,
                job_json=profile.model_dump(),
            )
            db.add(entity)
            db.commit()
            db.refresh(entity)
            app_logger.success(f"Job saved successfully. id={entity.id}")
            return entity
        except Exception:
            db.rollback()
            app_logger.exception("Failed to save job.")
            raise
        finally:
            db.close()

    # ----------------------------------------------------

    def get_latest(self):
        db = SessionLocal()
        try:
            return db.query(JobEntity).order_by(JobEntity.created_at.desc()).first()
        finally:
            db.close()

    # -----------------------------------------------------

    def delete_all(self):
        app_logger.info("Deleting all jobs.")
        db: Session = SessionLocal()
        try:
            db.query(JobEntity).delete()
            db.commit()
            app_logger.success("All jobs deleted.")
        finally:
            db.close()

    # -----------------------------------------------------

    def get_by_id(
        self,
        job_id: uuid.UUID,
    ) -> JobEntity | None:
        db = SessionLocal()
        try:
            return (
            db.query(JobEntity)
            .filter(JobEntity.id == job_id)
            .first()
        )
        finally:
            db.close()       

    def get_by_hash(
        self,
        url_hash: str,
    ):
        db = SessionLocal()
        try:
            return (
            db.query(
                JobEntity
            )
            .filter(
                JobEntity.url_hash == url_hash
            )
            .first()
            )   
        finally:
            db.close()