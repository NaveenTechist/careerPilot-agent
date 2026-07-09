"""
Application Repository.

Responsible only for database operations.

Responsibilities
----------------
- Save Application
- Get Latest Application
- Get By ID
- List Applications
- Update Status
"""

from uuid import UUID

from sqlalchemy.orm import Session

from database.database import SessionLocal

from models.db.application_entity import (
    ApplicationEntity,
    ApplicationStatus,
)

from core.logger import app_logger


class ApplicationRepository:

    # ----------------------------------------

    def save(
        self,
        resume_id: UUID,
        job_id: UUID,
        match_id: UUID,
        title: str,
    ) -> ApplicationEntity:

        app_logger.info(
            "Saving application."
        )

        db: Session = SessionLocal()
        try:
            entity = ApplicationEntity(
                resume_id=resume_id,
                job_id=job_id,
                match_id=match_id,
                title=title,
                status=ApplicationStatus.READY
            )

            db.add(entity)
            db.commit()
            db.refresh(entity)
            app_logger.success(
                f"Application created. id={entity.id}"
            )

            return entity

        except Exception:

            db.rollback()

            app_logger.exception(
                "Unable to save application."
            )

            raise

        finally:

            db.close()

    # ----------------------------------------

    def get_latest(self):

        db = SessionLocal()

        try:

            return (

                db.query(ApplicationEntity)

                .order_by(
                    ApplicationEntity.created_at.desc()
                )

                .first()

            )

        finally:

            db.close()

    # ----------------------------------------

    def get_by_id(
        self,
        application_id: UUID,
    ):
        db = SessionLocal()
        try:
            return (
                db.query(ApplicationEntity)
                .filter(
                    ApplicationEntity.id == application_id
                )
                .first()
            )
        finally:
            db.close()

    # ----------------------------------------

    def get_all(self):

        db = SessionLocal()

        try:

            return (

                db.query(ApplicationEntity)

                .order_by(
                    ApplicationEntity.created_at.desc()
                )

                .all()

            )

        finally:

            db.close()

    # ----------------------------------------

    def update_status(
        self,
        application_id: UUID,
        status: ApplicationStatus,
    ):

        db = SessionLocal()

        try:

            entity = (

                db.query(ApplicationEntity)

                .filter(
                    ApplicationEntity.id == application_id
                )
                .first()
            )
            if entity is None:
                return None
            entity.status = status
            db.commit()
            db.refresh(entity)
            app_logger.success(
                f"Application status updated to {status.value}"
            )
            return entity
        except Exception:
            db.rollback()
            app_logger.exception(
                "Unable to update application."
            )
            raise
        finally:
            db.close()