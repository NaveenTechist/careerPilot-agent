"""
CareerPilot Agent API.
"""

from fastapi import FastAPI

from api.resume import router as resume_router
from api.job import router as job_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from api.session import router as session_router
from api.matching import router as matching_router
from api.application import router as application_router
from database.init_db import init_database

init_database()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
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
