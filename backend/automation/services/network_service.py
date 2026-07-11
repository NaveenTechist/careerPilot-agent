import requests


class NetworkService:

    @staticmethod
    def is_online():

        try:

            requests.get(
                "https://www.google.com",
                timeout=5,
            )

            return True

        except Exception:

            return False