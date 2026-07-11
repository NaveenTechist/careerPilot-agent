"""
Text utilities used by
automation detectors.
"""

import re


class TextUtils:

    @staticmethod
    def normalize(
        text: str | None,
    ) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(
            r"\s+",
            " ",
            text,
        )
        return text.strip()