"""
Matching Normalizer.

Normalizes Gemini output.
"""


class MatchingNormalizer:

    @staticmethod
    def normalize(
        data: dict,
    ) -> dict:

        data.setdefault(
            "matched_skills",
            [],
        )

        data.setdefault(
            "missing_skills",
            [],
        )

        data.setdefault(
            "strengths",
            [],
        )

        data.setdefault(
            "weaknesses",
            [],
        )

        data.setdefault(
            "recommendation",
            "",
        )

        data.setdefault(
            "should_apply",
            False,
        )

        return data