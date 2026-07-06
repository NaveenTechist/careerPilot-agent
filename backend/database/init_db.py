from database.database import engine
from database.base import Base
from core.logger import app_logger

# Import entities
from models.db.resume_entity import ResumeEntity
from models.db.job_entity import JobEntity

app_logger.info("Initializing database.")


def init_database():
    Base.metadata.create_all(bind=engine)


app_logger.success("Database initialized successfully.")
