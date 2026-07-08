"""
Hashing Service.

Responsible only for generating hashes.
"""

from __future__ import annotations

import hashlib


class HashingService:

    @staticmethod
    def bytes_sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def text_sha256(text: str) -> str:
        normalized = " ".join(
            text.lower().split()
        )

        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()