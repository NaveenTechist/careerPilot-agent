"""
Prompt Loader

Loads prompt templates from disk.

Why?

- Keeps prompts outside Python code.
- Easy prompt tuning.
- Version control friendly.
"""
from pathlib import Path


class PromptLoader:
    """Utility class for loading prompt templates."""
    PROMPT_DIR = Path(__file__).parent / "prompts"
    @classmethod
    def load(cls, filename: str) -> str:
        """
        Load a prompt template.

        Parameters
        ----------
        filename : str
            Prompt filename.

        Returns
        -------
        str
            Prompt content.
        """

        prompt_path = cls.PROMPT_DIR / filename
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt '{filename}' not found.")
        return prompt_path.read_text(encoding="utf-8")
