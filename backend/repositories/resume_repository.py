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

from models.resume_profile import ResumeProfile
from models.db.resume_entity import ResumeEntity

from core.logger import app_logger


class ResumeRepository:

    def save(
        self,
        profile: ResumeProfile,
    ) -> ResumeEntity:

        app_logger.info(
            "Saving resume profile."
        )

        db: Session = SessionLocal()

        try:

            entity = ResumeEntity(
                name=profile.name,
                email=profile.email,
                phone=profile.phone,
                location=profile.location,
                resume_json=profile.model_dump(),
            )

            db.add(entity)
            db.commit()
            db.refresh(entity)

            app_logger.success(
                f"Resume saved successfully. id={entity.id}"
            )

            return entity

        except Exception:

            db.rollback()

            app_logger.exception(
                "Failed to save resume."
            )

            raise

        finally:

            db.close()

    # -----------------------------------------------------

    def get_latest(
        self,
    ) -> ResumeProfile | None:

        app_logger.info(
            "Fetching latest resume."
        )

        db: Session = SessionLocal()

        try:

            entity = db.scalar(

                select(
                    ResumeEntity
                ).order_by(
                    ResumeEntity.created_at.desc()
                )

            )

            if entity is None:

                app_logger.warning(
                    "No resume found."
                )

                return None

            app_logger.success(
                "Resume retrieved."
            )

            return ResumeProfile.model_validate(
                entity.resume_json
            )

        finally:

            db.close()

    # -----------------------------------------------------

    def delete_all(self):

        app_logger.info(
            "Deleting all resumes."
        )

        db: Session = SessionLocal()

        try:

            db.query(
                ResumeEntity
            ).delete()

            db.commit()

            app_logger.success(
                "All resumes deleted."
            )

        finally:

            db.close()