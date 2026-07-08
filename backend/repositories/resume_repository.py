"""
Resume Repository.

Responsible only for database operations.

Responsibilities
----------------
- Save Resume
- Get Latest Resume
- Get Resume By ID
- Delete Resume
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.db.resume_entity import ResumeEntity

from models.resume_profile import ResumeProfile
from models.db.resume_entity import ResumeEntity

from core.logger import app_logger


class ResumeRepository:
    def save(
        self,
        profile: ResumeProfile,
        file_hash: str | None = None,
        content_hash: str | None = None,
    ) -> ResumeEntity:
        if file_hash is None:
            from services.hashing_service import HashingService
            file_hash = HashingService.text_sha256(profile.name + (profile.email or ""))
        if content_hash is None:
            from services.hashing_service import HashingService
            content_hash = HashingService.text_sha256(str(profile.model_dump()))

        app_logger.info("Saving resume profile.")

        db: Session = SessionLocal()

        try:
            entity = ResumeEntity(
                name=profile.name,
                email=profile.email,
                phone=profile.phone,
                location=profile.location,
                resume_json=profile.model_dump(),
                file_hash=file_hash,
                content_hash=content_hash,
            )

            db.add(entity)
            db.commit()
            db.refresh(entity)

            app_logger.success(f"Resume saved successfully. id={entity.id}")

            return entity

        except Exception:
            db.rollback()

            app_logger.exception("Failed to save resume.")

            raise

        finally:
            db.close()

    # -----------------------------------------------------

    def get_latest(self):
        db = SessionLocal()
        try:
            return (
                db.query(ResumeEntity).order_by(ResumeEntity.created_at.desc()).first()
            )
        finally:
            db.close()

    # -----------------------------------------------------

    def delete_all(self):

        app_logger.info("Deleting all resumes.")
        db: Session = SessionLocal()
        try:
            db.query(ResumeEntity).delete()

            db.commit()

            app_logger.success("All resumes deleted.")

        finally:
            db.close()

    def get_by_hash(
        self,
        resume_hash: str,
    ):
        db: Session = SessionLocal()

        try:
            stmt = select(ResumeEntity).where(
                (ResumeEntity.file_hash == resume_hash) | (ResumeEntity.content_hash == resume_hash)
            )

            result = db.execute(stmt)
            entity = result.scalar_one_or_none()

            if entity is None:
                raise ValueError("No resume found with the provided hash.")

            return entity

        except Exception:
            db.rollback()

            app_logger.exception("Failed to get resume by hash.")

            raise

        finally:
            db.close()

    def get_by_file_hash(
        self,
        file_hash: str,
    ):
        db = SessionLocal()
        try:
            return (
                db.query(
                    ResumeEntity
                )
            .filter(
                ResumeEntity.file_hash == file_hash
            )
            .first()
            )
        finally:
            db.close()