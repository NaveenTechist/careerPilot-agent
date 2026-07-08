"""
Application Agent.
Coordinates the complete application workflow.
Responsibilities
----------------
- Process Resume
- Process Job
- Match Resume & Job
- Return Application
"""

from pathlib import Path

from agents.resume_agent import ResumeAgent
from agents.job_agent import JobAgent
from agents.matching_agent import MatchingAgent
from core.logger import app_logger



class ApplicationAgent:
    def __init__(
        self,
        resume_agent: ResumeAgent,
        job_agent: JobAgent,
        matching_agent: MatchingAgent,
    ):
        self.resume_agent = resume_agent
        self.job_agent = job_agent
        self.matching_agent = matching_agent

    def process(
        self,
        resume_path: Path,
        job_url: str,
    ):
        app_logger.info(
            "Application workflow started."
        )
        # ---------------------------------
        # Resume
        # ---------------------------------
        resume = self.resume_agent.process_resume(
            resume_path
        )
        # ---------------------------------
        # Job
        # ---------------------------------
        job = self.job_agent.process(
            job_url
        )
        # ---------------------------------
        # Match
        # ---------------------------------
        match = self.matching_agent.process()
        app_logger.success(
            "Application workflow completed."
        )
        return {
            "resume": resume,
            "job": job,
            "match": match,
        }