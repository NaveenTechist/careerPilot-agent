"""
Application configuration.

Centralized settings for the entire application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "CareerPilot Agent"
    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-2.5-flash"

    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5 MB
    TEMP_DIRECTORY: str = "temp"
    DATABASE_URL: str
    
    MIN_JOB_TEXT_LENGTH: int = 500
    PLAYWRIGHT_TIMEOUT: int = 30000
    HEADLESS_BROWSER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
