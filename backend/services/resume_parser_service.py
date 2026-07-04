"""
Resume Parser Service.
"""

from models.resume_profile import ResumeProfile
from core.exceptions import ResumeParsingError

from services.base_llm_parser_service import (
    BaseLLMParserService,
)

from services.resume_normalizer import (
    ResumeNormalizer,
)


class ResumeParserService(BaseLLMParserService):
    PROMPT_FILE = "resume_parser.md"
    MODEL = ResumeProfile
    NORMALIZER = ResumeNormalizer
    PARSING_EXCEPTION = ResumeParsingError


# """
# Resume Parser Service.

# Converts raw resume text into
# a structured ResumeProfile using Gemini.
# """

# import json

# from pydantic import ValidationError

# from core.logger import app_logger
# from core.exceptions import ResumeParsingError
# from llm.gemini_client import GeminiClient
# from llm.prompt_loader import PromptLoader
# from models.resume_profile import ResumeProfile
# from services.resume_normalizer import ResumeNormalizer

# class ResumeParserService:

#     def __init__(self):

#         self.client = GeminiClient()

#     def parse(self, resume_text: str) -> ResumeProfile:

#         app_logger.info(
#             "Loading resume parser prompt."
#         )

#         prompt = PromptLoader.load(
#             "resume_parser.md"
#         )

#         prompt = prompt.replace(
#             "{{resume}}",
#             resume_text,
#         )

#         app_logger.info(
#             "Sending prompt to Gemini."
#         )

#         response = self.client.generate(
#             prompt
#         )

#         app_logger.info(
#             "Cleaning Gemini response."
#         )

#         cleaned = self._clean_json(
#             response
#         )

#         try:

#             data = json.loads(cleaned)
#             app_logger.info(
#                 "Normalizing Gemini response."
#             )

#             normalized = ResumeNormalizer.normalize(
#                 data
#             )

#             profile = ResumeProfile.model_validate(
#                 normalized
#             )

#             app_logger.success(
#                     f"""
#                     Resume parsed successfully.
#                     Skills : {len(profile.skills)}
#                     Projects : {len(profile.projects)}
#                     Experience : {len(profile.experience)}
#                     Education : {len(profile.education)}
#                 """
#                 )
#             return profile

#         except (
#             json.JSONDecodeError,
#             ValidationError,
#         ) as e:

#             app_logger.exception(
#                 "Resume parsing failed."
#             )

#             raise ResumeParsingError(
#                 "Invalid response returned by Gemini."
#             ) from e


#     def _clean_json(
#         self,
#         response: str,
#     ) -> str:
#         """
#         Remove markdown code blocks.
#         Gemini sometimes returns
#         ```json
#         { ... }
#         ```
#         We only want JSON.
#         """

#         response = response.strip()
#         if response.startswith("```json"):
#             response = response.replace(
#                 "```json",
#                 "",
#                 1,
#             )

#         if response.endswith("```"):
#             response = response[:-3]

#         return response.strip()
