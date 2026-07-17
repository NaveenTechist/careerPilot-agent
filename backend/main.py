"""
CareerPilot Agent API.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.resume import router as resume_router
from api.job import router as job_router
from core.config import settings
from api.session import router as session_router
from api.matching import router as matching_router
from api.application import router as application_router
from database.init_db import init_database
from core.exceptions import (
    CareerPilotError,
    InvalidResumeError,
    ResumeExtractionError,
    ResumeParsingError,
    JobScrapingError,
    JobParsingError,
    LLMServiceError,
    MatchingError,
)
from core.logger import app_logger

init_database()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.exception_handler(CareerPilotError)
async def careerpilot_error_handler(request: Request, exc: CareerPilotError):
    """
    Global exception handler for all application-specific errors.
    Translates them into clean HTTP JSON responses.
    """
    app_logger.error(f"Application error caught by handler: {exc.__class__.__name__} - {str(exc)}")

    status_code = 500
    if isinstance(exc, InvalidResumeError):
        status_code = 400
    elif isinstance(exc, JobScrapingError):
        status_code = 400
    elif isinstance(exc, ResumeExtractionError):
        status_code = 422
    elif isinstance(exc, ResumeParsingError):
        status_code = 422
    elif isinstance(exc, JobParsingError):
        status_code = 422
    elif isinstance(exc, MatchingError):
        status_code = 422
    elif isinstance(exc, LLMServiceError):
        if "rate limit" in str(exc).lower():
            status_code = 429
        else:
            status_code = 503

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(job_router)
app.include_router(session_router)
app.include_router(matching_router)
app.include_router(application_router)

@app.get("/")
def root():
    return {"message": "CareerPilot Agent Running..."}


@app.get("/health")
def health():
    return {"status": "healthy"}
