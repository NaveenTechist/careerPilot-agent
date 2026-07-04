class MatchingAgent:

    def __init__(
        self,
        matching_service,
    ):

        self.matching_service = matching_service

    def process(
        self,
        resume,
        job,
    ):

        return self.matching_service.match(
            resume,
            job,
        )