class MatchingService:
    def __init__(self):

        self.parser = MatchingParserService()

    def match(
        self,
        resume,
        job,
    ):

        prompt = f"""
Resume

{resume.model_dump_json(indent=2)}

Job

{job.model_dump_json(indent=2)}
"""

        return self.parser.parse(prompt)
