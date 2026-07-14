from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile
from core.config import settings
STORAGE_DIRECTORY = "storage"


class StorageService:

    ROOT = Path(settings.STORAGE_DIRECTORY) / "resumes"

    @classmethod
    def save_resume(
        cls,
        upload: UploadFile,
    ) -> str:

        cls.ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = Path(
            upload.filename
        ).suffix

        filename = f"{uuid.uuid4()}{extension}"

        destination = cls.ROOT / filename

        with destination.open("wb") as buffer:

            shutil.copyfileobj(
                upload.file,
                buffer,
            )

        return str(destination)

    # ------------------------------------

    @staticmethod
    def delete_resume(
        path: str,
    ):

        file = Path(path)

        if file.exists():

            file.unlink()