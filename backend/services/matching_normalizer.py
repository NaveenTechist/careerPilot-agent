"""
Matching Normalizer.

Normalizes Gemini output before
Pydantic validation.
"""

from copy import deepcopy

class MatchingNormalizer:
    @classmethod
    def normalize(
        cls,
        data: dict,
    ) -> dict:
        data = deepcopy(data)
        cls._normalize_root(data)
        return data
    @staticmethod
    def _normalize_root(
        data: dict,
    ):
        STRING_FIELDS = {
            "overall_level",
            "recommendation",
        }
        for field in STRING_FIELDS:
            if data.get(field) is None:
                data[field] = ""
        LIST_FIELDS = {
            "matched_skills",
            "missing_skills",
            "strengths",
            "weaknesses",
            "next_steps",
        }
        for field in LIST_FIELDS:
            value = data.get(field)
            if value is None:
                data[field] = []
            elif isinstance(
                value,
                str,
            ):
                data[field] = [value]
            elif not isinstance(
                value,
                list,
            ):
                data[field] = []
        if data.get("score") is None:
            data["score"] = 0
        if data.get("should_apply") is None:
            data["should_apply"] = False