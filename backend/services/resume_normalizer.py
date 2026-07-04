"""
Resume Normalizer

Purpose
-------
Gemini is an LLM.

Even when instructed to return JSON,
it may slightly change field names.

This class normalizes Gemini's output
before validating with Pydantic.
"""

from copy import deepcopy


class ResumeNormalizer:
    """
    Normalizes Gemini response into
    ResumeProfile format.
    """

    @classmethod
    def normalize(cls, data: dict) -> dict:

        data = deepcopy(data)
        cls._normalize_education(data)
        cls._normalize_experience(data)
        cls._normalize_root(data)
        cls._normalize_projects(data)
        cls._normalize_certifications(data)
        return data

    @staticmethod
    def _normalize_education(data: dict):
        education = data.get("education", [])
        for item in education:
            item["institution"] = (
                item.get("institution")
                or item.get("college")
                or item.get("school")
                or item.get("university")
                or ""
            )
            item.setdefault("specialization", None)
            item.setdefault("start_date", None)
            item.setdefault("end_date", None)
            item["grade"] = (
                item.get("grade") or item.get("gpa") or item.get("cgpa") or None
            )

    @staticmethod
    def _normalize_experience(data: dict):
        experience = data.get("experience", [])
        for item in experience:
            item["role"] = (
                item.get("role") or item.get("title") or item.get("position") or ""
            )
            item.setdefault("company", "")
            item.setdefault("start_date", None)
            item.setdefault("end_date", None)
            item.setdefault("location", None)
            responsibilities = item.get("responsibilities", [])
            if isinstance(
                responsibilities,
                str,
            ):
                responsibilities = [responsibilities]

            item["responsibilities"] = responsibilities

    @staticmethod
    def _normalize_projects(data: dict):
        projects = data.get("projects", [])
        for project in projects:
            project["title"] = project.get("title") or project.get("name") or ""
            description = project.get("description", "")
            if isinstance(
                description,
                list,
            ):
                description = "\n".join(description)
            project["description"] = description

            technologies = project.get("technologies", [])
            if isinstance(
                technologies,
                str,
            ):
                technologies = [technologies]

            project["technologies"] = technologies

            project.setdefault(
                "github",
                None,
            )

            project.setdefault(
                "live_url",
                None,
            )

    @staticmethod
    def _normalize_certifications(data: dict):
        certifications = data.get("certifications", [])
        normalized = []
        for cert in certifications:
            if isinstance(cert, str):
                normalized.append(cert)
            elif isinstance(cert, dict):
                normalized.append(
                    cert.get("name")
                    or cert.get("title")
                    or cert.get("certificate")
                    or ""
                )
        data["certifications"] = normalized

    @staticmethod
    def _normalize_root(data: dict):

            # ---------- Strings ----------

            STRING_FIELDS = {
                "name",
                "email",
                "phone",
                "location",
                "summary",
                "linkedin",
                "github",
                "portfolio",
            }
            for field in STRING_FIELDS:
                if data.get(field) is None:
                    data[field] = ""
            # ---------- Lists ----------
            LIST_FIELDS = {
                "skills",
                "languages",
                "education",
                "experience",
                "projects",
                "certifications",
            }
            for field in LIST_FIELDS:
                value = data.get(field)
                if value is None:
                    data[field] = []
                elif isinstance(value, str):
                    data[field] = [value]
                elif not isinstance(value, list):
                    data[field] = []    
