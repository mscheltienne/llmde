from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .utils._checks import ensure_path

if TYPE_CHECKING:
    from pathlib import Path


def read_prompt(path: str | Path) -> str:
    """Read a prompt from a file.

    Parameters
    ----------
    path : str | Path
        The path to the prompt file.
    """
    path = ensure_path(path, must_exist=True)
    with open(path, encoding="utf-8") as fid:
        return fid.read()


def read_json_schema(path: str | Path) -> dict:
    """Read a JSON schema from a file.

    Parameters
    ----------
    path : str | Path
        The path to the JSON schema file.
    """
    path = ensure_path(path, must_exist=True)
    with open(path, encoding="utf-8") as fid:
        return json.load(fid)
