from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

from ..io import read_markdown
from ..utils._checks import check_type, ensure_path

if TYPE_CHECKING:
    from pathlib import Path


class BaseModel(ABC):
    """Abstract base class for all models."""

    def __init__(
        self,
        model_name: str,
        api_key: str,
        *,
        system_instruction: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        max_tokens: int = 8192,
    ) -> None:
        """Initialize the model with the given model name and configuration.

        Parameters
        ----------
        model_name : str
            The name of the model to use.
        api_key : str
            The API key for accessing the model.
        system_instruction : str | None
            System instruction to provide high-level context and behavioral guidance to
            the model. For data extraction tasks, this can define the model's persona
            (e.g., systematic review researcher) and establish extraction principles.
        temperature : float | None
            Controls randomness in token selection during response generation. Ranges
            from ``0.0`` to ``1.0``. Lower values produce more deterministic, focused
            outputs by favoring high-probability tokens. Higher values (approaching
            ``1.0``) increase diversity and creativity. For factual data extraction
            where consistency and accuracy are paramount, use ``temperature=0.0``.
        top_p : float | None
            Nucleus sampling parameter. Tokens are selected from highest to lowest
            probability until their cumulative probability reaches this threshold.
            Ranges from ``0.0`` to ``1.0``. Lower values restrict sampling to
            higher-probability tokens, reducing randomness. For deterministic outputs,
            use a low value (e.g., ``0.0``) or leave as ``None`` to use the API default.
        top_k : int | None
            Restricts sampling to the ``top_k`` most probable tokens at each step.
            Must be ``>= 1``. A value of ``1`` implements greedy decoding, always
            selecting the most probable token. Lower values reduce randomness. For
            maximum determinism, use ``top_k=1``.
        max_tokens : int
            Maximum number of tokens to generate in the response. Defaults to ``8192``.
            Set this high enough to accommodate the expected JSON output size for data
            extraction tasks.

        Notes
        -----
        **Recommended settings for deterministic data extraction:**

        For systematic reviews and scientific data extraction where reproducibility and
        accuracy are critical, configure the model to minimize randomness:

        - ``temperature=0.0``: Favors the highest-probability tokens, producing the
          most deterministic outputs. This is the primary parameter to adjust.
        - ``top_k=1``: Greedy decoding - always selects the single most probable token.
          Eliminates randomness from the "long tail" of low-probability tokens.
        - ``top_p=0.0`` or ``None``: When set very low, further restricts sampling to
          only the most probable tokens.

        **Parameter interaction:**

        These parameters work sequentially in the sampling pipeline:

        1. ``top_k`` first narrows candidates to the K most probable tokens
        2. ``top_p`` then filters by cumulative probability threshold
        3. ``temperature`` makes the final selection from remaining candidates

        **Important considerations:**

        - Even with ``temperature=0.0``, outputs may not be fully deterministic due to
          floating-point operations and GPU parallelism.
        - Most APIs recommend adjusting ``temperature`` first. Only modify ``top_k`` or
          ``top_p`` for advanced use cases.
        - Some APIs recommend using either ``temperature`` or ``top_p``, not both
          simultaneously.

        See https://towardsdatascience.com/how-to-write-expert-prompts-for-chatgpt-gpt-4-and-other-language-models-23133dc85550/
        for prompt engineering tips and best practices.
        """
        check_type(model_name, (str,), "model_name")
        check_type(api_key, (str,), "api_key")
        self._model_name = model_name

        # Validate system_instruction
        check_type(system_instruction, (str, None), "system_instruction")

        # Validate temperature
        check_type(temperature, ("numeric", None), "temperature")
        if temperature is not None and (temperature < 0.0 or temperature > 1.0):
            raise ValueError(
                f"Temperature must be between 0.0 and 1.0. Provided {temperature} is "
                "invalid."
            )

        # Validate top_p
        check_type(top_p, ("numeric", None), "top_p")
        if top_p is not None and (top_p < 0.0 or top_p > 1.0):
            raise ValueError(
                f"top_p must be between 0.0 and 1.0. Provided {top_p} is invalid."
            )

        # Validate top_k
        check_type(top_k, ("int-like", None), "top_k")
        if top_k is not None and top_k < 1:
            raise ValueError(f"top_k must be >= 1. Provided {top_k} is invalid.")

        # Validate max_tokens
        check_type(max_tokens, ("int-like",), "max_tokens")
        if max_tokens <= 0:
            raise ValueError(
                f"max_tokens must be a positive integer. Provided {max_tokens} is "
                "invalid."
            )

    @abstractmethod
    def query(self, prompt: str, files: list[str | Path]) -> tuple[str, list[Path]]:
        """Query the model with a given prompt and return the response."""
        prompt = read_markdown(prompt)
        check_type(files, (Iterable,), "files")
        files = [ensure_path(file, must_exist=True) for file in files]
        return prompt, files

    @property
    def model_name(self) -> str:
        """Get the name of the model."""
        return self._model_name
