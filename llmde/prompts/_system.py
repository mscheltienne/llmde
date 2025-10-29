from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING

from ..utils._checks import check_type, check_value

if TYPE_CHECKING:
    from pathlib import Path

ASSETS_DIRECTORY = files("llmde.prompts") / "assets" / "system"


def list_system_instruction() -> list[str]:
    """List all system instruction files in the assets directory."""
    return [
        file.stem
        for file in ASSETS_DIRECTORY.iterdir()
        if file.is_file() and file.suffix == ".md"
    ]


def get_system_instruction(name: str) -> tuple[Path, Path | None]:
    """Get the path to a specific system instruction file by name.

    Parameters
    ----------
    name : str
        The name of the prompt file (without path).

    Returns
    -------
    prompt_path : Path
        The path to the prompt file.
    """
    check_type(name, (str,), "name")
    check_value(name, list_system_instruction(), "name")
    prompt_path = ASSETS_DIRECTORY / f"{name}.md"
    return prompt_path
