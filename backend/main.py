"""
CareerPilot Agent API.
"""

from fastapi import FastAPI

from api.resume import router as resume_router
from api.job import router as job_router
from core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(resume_router)
app.include_router(job_router)


@app.get("/")
def root():
    return {"message": "CareerPilot Agent Running..."}


@app.get("/health")
def health():
    return {"status": "healthy"}
