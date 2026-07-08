import hashlib

class HashingService:

    @staticmethod
    def sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
    @staticmethod
    def text_sha256(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()