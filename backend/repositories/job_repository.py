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


class JobRepository:

    def save(
        self,
        profile: JobProfile,
    ) -> JobEntity:

        app_logger.info(
            "Saving job profile."
        )

        db: Session = SessionLocal()

        try:

            entity = JobEntity(

                company=profile.company,

                job_title=profile.job_title,

                application_url=profile.application_url,

                job_json=profile.model_dump(),

            )

            db.add(entity)

            db.commit()

            db.refresh(entity)

            app_logger.success(
                f"Job saved successfully. id={entity.id}"
            )

            return entity

        except Exception:

            db.rollback()

            app_logger.exception(
                "Failed to save job."
            )

            raise

        finally:

            db.close()

    # -----------------------------------------------------

    def get_latest(
        self,
    ) -> JobProfile | None:

        app_logger.info(
            "Fetching latest job."
        )

        db: Session = SessionLocal()

        try:

            entity = db.scalar(

                select(
                    JobEntity
                ).order_by(
                    JobEntity.created_at.desc()
                )

            )

            if entity is None:

                app_logger.warning(
                    "No job found."
                )

                return None

            app_logger.success(
                "Job retrieved."
            )

            return JobProfile.model_validate(
                entity.job_json
            )

        finally:

            db.close()

    # -----------------------------------------------------

    def delete_all(self):

        app_logger.info(
            "Deleting all jobs."
        )

        db: Session = SessionLocal()

        try:

            db.query(
                JobEntity
            ).delete()

            db.commit()

            app_logger.success(
                "All jobs deleted."
            )

        finally:

            db.close()