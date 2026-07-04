"""
Job Normalizer.

Normalizes Gemini job output.
"""

from copy import deepcopy


class JobNormalizer:
    @classmethod
    def normalize(
        cls,
        data: dict,
    ) -> dict:

        data = deepcopy(data)

        data.setdefault(
            "company",
            None,
        )
        data.setdefault(
            "location",
            None,
        )
        data.setdefault(
            "employment_type",
            None,
        )
        data.setdefault(
            "salary",
            None,
        )
        data.setdefault(
            "education",
            None,
        )
        data.setdefault(
            "experience",
            None,
        )
        data.setdefault(
            "application_url",
            None,
        )

        data.setdefault(
            "required_skills",
            [],
        )
        data.setdefault(
            "preferred_skills",
            [],
        )

        data.setdefault(
            "responsibilities",
            [],
        )
        data.setdefault(
            "benefits",
            [],
        )
        return data
