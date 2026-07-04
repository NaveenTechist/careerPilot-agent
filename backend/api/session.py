from fastapi import APIRouter

from services.session_service import session

router = APIRouter(
    prefix="/session",
    tags=["Session"],
)


@router.get("/")
def current_session():

    s = session.session

    return {

        "status": s.status,

        "resume": {

            "uploaded": s.resume is not None,

            "profile": (

                {

                    "name": s.resume.name,

                    "skills": len(s.resume.skills),

                    "projects": len(s.resume.projects),

                    "experience": len(s.resume.experience),

                }

                if s.resume

                else None

            ),

        },

        "job": {

            "uploaded": s.job is not None,

            "profile": (

                {

                    "company": s.job.company,

                    "title": s.job.job_title,

                    "required_skills": len(
                        s.job.required_skills
                    ),

                }

                if s.job

                else None

            ),

        },
        "next_action": (

            s.status.value

        ),
    }