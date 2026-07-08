from pydantic import BaseModel
from pydantic import HttpUrl


class ApplicationRequest(BaseModel):

    job_url: HttpUrl