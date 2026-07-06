from fastapi import APIRouter

from repositories.resume_repository import ResumeRepository
from repositories.job_repository import JobRepository

router = APIRouter(
    prefix="/session",
    tags=["Session"],
)


@router.get("/")
def current_session():

    resume = ResumeRepository().get_latest()

    job = JobRepository().get_latest()

    if resume and job:
        status = "READY_FOR_MATCHING"

    elif resume:
        status = "WAITING_FOR_JOB"

    else:
        status = "WAITING_FOR_RESUME"

    return {
        "status": status,
        "resume": {
            "uploaded": resume is not None,
            "profile": (
                {
                    "name": resume.name,
                    "skills": len(
                        resume.resume_json.get(
                            "skills",
                            [],
                        )
                    ),
                    "projects": len(
                        resume.resume_json.get(
                            "projects",
                            [],
                        )
                    ),
                    "experience": len(
                        resume.resume_json.get(
                            "experience",
                            [],
                        )
                    ),
                }
                if resume
                else None
            ),
        },
        "job": {
            "uploaded": job is not None,
            "profile": (
                {
                    "company": job.company,
                    "title": job.job_title,
                    "required_skills": len(
                        job.job_json.get(
                            "required_skills",
                            [],
                        )
                    ),
                }
                if job
                else None
            ),
        },
        "next_action": status,
    }
