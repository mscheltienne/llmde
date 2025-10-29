from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING

from ..utils._checks import check_type, check_value

if TYPE_CHECKING:
    from pathlib import Path

ASSETS_DIRECTORY = files("llmde.prompts") / "assets" / "prompts"


def list_prompt_files() -> list[str]:
    """List all prompt files in the assets directory."""
    return [
        file.stem
        for file in ASSETS_DIRECTORY.iterdir()
        if file.is_file() and file.suffix == ".md"
    ]


def get_prompt(name: str) -> tuple[Path, Path | None]:
    """Get the path to a specific prompt file by name.

    Parameters
    ----------
    name : str
        The name of the prompt file (without path).

    Returns
    -------
    prompt_path : Path
        The path to the prompt file.
    json_path : Path | None
        The path to the JSON schema file for the prompt, if applicable.
    """
    check_type(name, (str,), "name")
    check_value(name, list_prompt_files(), "name")
    prompt_path = ASSETS_DIRECTORY / f"{name}.md"
    json_path = ASSETS_DIRECTORY / f"{name}.json"
    return prompt_path, json_path if json_path.exists() else None
