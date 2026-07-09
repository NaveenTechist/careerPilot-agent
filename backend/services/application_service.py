"""
Application Service.

Orchestrates the complete workflow.

Responsible for

- Resume Parsing
- Job Parsing
- Resume Matching
- Database Transaction

Never

- HTTP
- HTML Scraping
- Gemini API
"""

from agents.resume_agent import ResumeAgent
from agents.job_agent import JobAgent
from agents.matching_agent import MatchingAgent
from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository
from repositories.match_repository import MatchRepository
from repositories.application_repository import ApplicationRepository
from core.logger import app_logger

class ApplicationService:

    def __init__(
        self,
        resume_agent,
        job_agent,
        matching_agent,
        resume_repository,
        job_repository,
        match_repository,
        application_repository,
    ):
        self.resume_agent = resume_agent
        self.job_agent = job_agent
        self.matching_agent = matching_agent
        self.resume_repository = resume_repository
        self.job_repository = job_repository
        self.match_repository = match_repository
        self.application_repository = application_repository 

    def create_application(
        self,
        resume_path,
        job_url,
    ):
        app_logger.info(f"Application Service: {resume_path}, {job_url}")
        
        resume_profile = self.resume_agent.process_resume(
            resume_path
        )

        job_profile = self.job_agent.process(
            job_url
        )

        match_result = self.matching_agent.match(
            resume_profile,
            job_profile
        )

        app_logger.info("Match result")

        resume_entity = self.resume_repository.save(
            resume_profile
        )   

        job_entity = self.job_repository.save(
            job_profile
        )
        match_entity = self.match_repository.save(

            resume_id=resume_entity.id,

            job_id=job_entity.id,

            result=match_result,

        )

        application = self.application_repository.save(

            resume_id=resume_entity.id,

            job_id=job_entity.id,
            match_id=match_entity.id,
            title=f"{job_profile.company} • {job_profile.job_title}",

        )

        app_logger.success("Application created successfully.")
        return {
            "id": str(application.id),
            "status": application.status,
            "message":"Application Created",
            "application_data": application,
        }