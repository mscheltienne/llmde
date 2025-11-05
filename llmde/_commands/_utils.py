from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ..io import read_markdown
from ..models import ClaudeModel, GeminiModel
from ..prompts import (
    get_prompt,
    get_system_instruction,
    list_prompt_files,
    list_system_instruction,
)
from ..utils._checks import ensure_path

if TYPE_CHECKING:
    from ..models._base import BaseModel

# Model name patterns and their corresponding classes
MODEL_MAPPING = {
    "claude": ClaudeModel,  # Matches any claude-*
    "gemini": GeminiModel,  # Matches any gemini-*
}


def get_model_class(model_name: str) -> type[BaseModel]:
    """Determine the model class from model name.

    Parameters
    ----------
    model_name : str
        Name of the model (e.g., "claude-sonnet-4-5-20250929").

    Returns
    -------
    type[BaseModel]
        Model class to use.

    Raises
    ------
    ValueError
        If model name doesn't match any known pattern.
    """
    model_lower = model_name.lower()
    for pattern, model_class in MODEL_MAPPING.items():
        if model_lower.startswith(pattern):
            return model_class

    raise ValueError(
        f"Unknown model: {model_name}. "
        f"Expected model name starting with: {list(MODEL_MAPPING.keys())}"
    )


def get_api_key(model_name: str, api_key: str | None) -> str:
    """Get API key from argument or environment variable.

    Parameters
    ----------
    model_name : str
        Name of the model.
    api_key : str | None
        API key from command line argument (or None).

    Returns
    -------
    str
        API key to use.

    Raises
    ------
    ValueError
        If no API key provided and not found in environment.
    """
    import os

    if api_key is not None:
        return api_key

    # Determine environment variable name based on model
    model_lower = model_name.lower()
    if model_lower.startswith("claude"):
        env_var = "LLMDE_CLAUDE_API_KEY"
    elif model_lower.startswith("gemini"):
        env_var = "LLMDE_GEMINI_API_KEY"
    else:
        raise ValueError(f"Unknown model type for API key lookup: {model_name}")

    api_key_from_env = os.getenv(env_var)
    if api_key_from_env is None:
        raise ValueError(
            f"API key not provided and environment variable {env_var} not set. "
            f"Either provide --api-key or set {env_var}."
        )

    return api_key_from_env


def get_prompt_path(prompt: str) -> tuple[Path, Path | None]:
    """Get prompt path from name or file path.

    Parameters
    ----------
    prompt : str
        Built-in name or file path.

    Returns
    -------
    prompt_path : Path
        Path to the prompt markdown file.
    json_schema_path : Path | None
        Path to the JSON schema file (or None if not found).

    Raises
    ------
    ValueError
        If prompt not found.
    """
    built_in_prompts = list_prompt_files()
    if prompt in built_in_prompts:
        # Try as built-in first
        prompt_path, json_schema_path = get_prompt(prompt)
    else:
        # Try as file path - validate and ensure it exists
        prompt_path = ensure_path(prompt, must_exist=True)
        # Check for corresponding JSON schema
        json_schema_path = prompt_path.with_suffix(".json")
        json_schema_path = json_schema_path if json_schema_path.exists() else None
    return prompt_path, json_schema_path


def get_system_instruction_text(system_instruction: str | None) -> str | None:
    """Get system instruction content from name or path.

    Parameters
    ----------
    system_instruction : str | None
        Built-in name or file path (or None to skip).

    Returns
    -------
    str | None
        System instruction text content (or None if skipped).

    Raises
    ------
    ValueError
        If system instruction not found.
    """
    if system_instruction is None:
        return None

    built_in_systems = list_system_instruction()
    if system_instruction in built_in_systems:
        # Try as built-in first
        system_path = get_system_instruction(system_instruction)
    else:
        # Try as file path - validate and ensure it exists
        system_path = ensure_path(system_instruction, must_exist=True)
    return read_markdown(system_path)
