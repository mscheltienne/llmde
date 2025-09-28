from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class BaseModel(ABC):
    """Abstract base class for all models."""

    def __init__(self, model_name: str) -> None:
        """Initialize the model with the given model name."""
        self.model_name = model_name

    @abstractmethod
    def query(self, prompt: str, files: list[str | Path]) -> str:
        """Query the model with a given prompt and return the response."""
