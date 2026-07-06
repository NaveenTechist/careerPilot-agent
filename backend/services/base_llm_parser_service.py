"""
Base LLM Parser Service.

This service contains the common AI parsing workflow.

Every parser (Resume, Job, Cover Letter, etc.)
inherits from this class.

Subclasses only need to provide:

- PROMPT_FILE
- MODEL
- NORMALIZER
"""

from __future__ import annotations

import json
from abc import ABC

from pydantic import ValidationError

from core.exceptions import CareerPilotError
from core.logger import app_logger
from llm.gemini_client import GeminiClient
from llm.prompt_loader import PromptLoader


class BaseLLMParserService(ABC):
    PROMPT_FILE: str = ""
    MODEL = None
    NORMALIZER = None
    PARSING_EXCEPTION = CareerPilotError

    def __init__(self):
        self.client = GeminiClient()

    def parse(self, text: str):
        # print("=" * 60)
        # print("CLASS =", type(self).__name__)
        # print("PROMPT_FILE =", repr(self.PROMPT_FILE))
        # print("=" * 60)
        app_logger.info(f"Loading prompt: {self.PROMPT_FILE}")
        prompt = PromptLoader.load(self.PROMPT_FILE)
        # print("=" * 80)
        # print("LOADED PROMPT")
        # print(prompt)
        # print("=" * 80)
        prompt = prompt.replace(
            "{{content}}",
            text,
        )
        response = self.client.generate(prompt)
        # print("=" * 80)
        # print("RAW GEMINI")
        # print(response)
        # print("=" * 80)
        cleaned = self._clean_json(response)
        # print("=" * 80)
        # print("CLEANED JSON")
        # print(cleaned)
        # print("=" * 80)
        try:
            data = json.loads(cleaned)
            normalized = self.NORMALIZER.normalize(data)
            # print("=")
            # print("NORMALIZED")
            # print(json.dumps(normalized, indent=2))
            # print("=")
            model = self.MODEL.model_validate(normalized)
            app_logger.success(f"{self.MODEL.__name__} parsed successfully.")
            # print("=" * 80)
            # print("After Parse Response", model)
            # print("=" * 80)

            return model

        except (
            json.JSONDecodeError,
            ValidationError,
        ) as e:
            app_logger.exception("Parser validation failed.")

            raise self.PARSING_EXCEPTION("Invalid LLM response.") from e

    @staticmethod
    def _clean_json(
        response: str,
    ) -> str:

        response = response.strip()
        if response.startswith("```json"):
            response = response.replace(
                "```json",
                "",
                1,
            )
        if response.endswith("```"):
            response = response[:-3]

        return response.strip()
