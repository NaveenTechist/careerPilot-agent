"""
Test Matching Parser.
"""

from services.matching_parser_service import (
    MatchingParserService,
)

parser = MatchingParserService()

resume = """
Python
FastAPI
Docker
Redis
Git
LLMs
"""

job = """
Python
FastAPI
Git
Docker
AWS
Redis
"""

prompt = f"""

Resume

{resume}

Job

{job}

"""

result = parser.parse(
    prompt
)

print(
    result.model_dump_json(
        indent=4
    )
)