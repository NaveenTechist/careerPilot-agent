"""
Custom exceptions used across the project.

Why?

Never expose third-party library exceptions directly to users.
Every external exception should be translated into a meaningful
business exception.
"""


class CareerPilotError(Exception):
    """Base exception for the application."""


class InvalidResumeError(CareerPilotError):
    """Raised when uploaded resume is invalid."""


class ResumeExtractionError(CareerPilotError):
    """Raised when resume text extraction fails."""


class ResumeParsingError(CareerPilotError):
    """Raised when Gemini cannot parse the resume."""


class JobScrapingError(CareerPilotError):
    """Raised when job page scraping fails."""


class JobParsingError(CareerPilotError):
    """Raised when AI fails to parse the job description."""


class LLMServiceError(CareerPilotError):
    """Raised when the LLM service is unavailable."""


class MatchingError(CareerPilotError):
    """Raised when resume matching fails."""
