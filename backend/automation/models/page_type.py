"""
Page Type.

Represents the detected state of the current
browser page during automation.

Used by PageDetector to classify what
the automation agent is looking at,
enabling deterministic state-machine
navigation instead of blind element checks.
"""

from enum import Enum


class PageType(str, Enum):

    # ------------------------------------------------
    # Job listing / landing page.
    # Contains job description + Apply button.
    # ------------------------------------------------
    LANDING = "LANDING"

    # ------------------------------------------------
    # Authentication required.
    # Password fields, login/sign-in forms visible.
    # ------------------------------------------------
    LOGIN = "LOGIN"

    # ------------------------------------------------
    # Apply entry point detected.
    # Apply / Easy Apply / Start Application visible.
    # ------------------------------------------------
    APPLY = "APPLY"

    # ------------------------------------------------
    # Active application form.
    # Editable fields (input, select, textarea) present.
    # ------------------------------------------------
    FORM = "FORM"

    # ------------------------------------------------
    # Review / preview page.
    # Summary of entered data before submission.
    # ------------------------------------------------
    REVIEW = "REVIEW"

    # ------------------------------------------------
    # Application submitted successfully.
    # Confirmation message detected.
    # ------------------------------------------------
    SUCCESS = "SUCCESS"

    # ------------------------------------------------
    # Error page.
    # Expired link, 404, access denied, job closed.
    # ------------------------------------------------
    ERROR = "ERROR"

    # ------------------------------------------------
    # Page is still loading.
    # Spinner, skeleton, AJAX overlay detected.
    # ------------------------------------------------
    LOADING = "LOADING"

    # ------------------------------------------------
    # Automation paused.
    # Requires user input for ambiguous questions
    # (salary, gender, veteran status, etc.)
    # ------------------------------------------------
    WAITING_USER = "WAITING_USER"

    # ------------------------------------------------
    # Could not classify the page.
    # Fallback state.
    # ------------------------------------------------
    UNKNOWN = "UNKNOWN"
