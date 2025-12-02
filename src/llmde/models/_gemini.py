from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import TYPE_CHECKING

from google import genai
from google.genai import types

from ..io import read_json_schema
from ._base import BaseModel

if TYPE_CHECKING:
    from pathlib import Path


class GeminiModel(BaseModel):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        *,
        system_instruction: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        max_tokens: int = 4096,
    ) -> None:
        """Initialize the Gemini model with the given model name and API key.

        Parameters
        ----------
        model_name : str
            The name of the Gemini model to use (e.g., ``"gemini-2.0-flash"``).
        api_key : str
            The API key for accessing the Gemini API.
        system_instruction : str | None
            System instruction to provide high-level context and behavioral guidance to
            the model. For data extraction tasks, this can define the model's persona
            (e.g., systematic review researcher) and establish extraction principles.
        temperature : float | None
            Controls randomness in token selection during response generation. Ranges
            from ``0.0`` to ``1.0`` (Gemini supports up to ``2.0``, but this package
            validates to ``1.0`` for cross-model consistency). Lower values produce more
            deterministic, focused outputs by favoring high-probability tokens. Higher
            values increase diversity and creativity. For factual data extraction where
            consistency and accuracy are paramount, use ``temperature=0.0``.
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
            Maximum number of tokens to generate in the response. Defaults to ``4096``.
            Set this high enough to accommodate the expected JSON output size for data
            extraction tasks.

        Notes
        -----
        **Gemini-specific considerations:**

        - Gemini supports JSON schema enforcement via ``response_json_schema`` in
          ``GenerateContentConfig``, which is used automatically when a JSON schema
          file is provided to the :meth:`~GeminiModel.query` method.
        - The parameters work sequentially: ``top_k`` narrows candidates first, then
          ``top_p`` filters by cumulative probability, and finally ``temperature``
          makes the selection.

        **Recommended settings for deterministic data extraction:**

        - ``temperature=0.0``: Primary parameter for deterministic outputs.
        - ``top_k=1``: Greedy decoding for maximum determinism.
        - ``top_p=0.0``: Further restricts to highest-probability tokens.

        See https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values
        for detailed parameter documentation and https://towardsdatascience.com/how-to-write-expert-prompts-for-chatgpt-gpt-4-and-other-language-models-23133dc85550/
        for prompt engineering tips and best practices.
        """  # noqa: E501
        super().__init__(
            model_name,
            api_key,
            system_instruction=system_instruction,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
        )
        self._client = genai.Client(
            api_key=api_key, http_options=types.HttpOptions(api_version="v1")
        )

        # Create Gemini-specific config dictionary
        # Note: Gemini API uses "max_output_tokens" instead of "max_tokens"
        self._config = {
            "system_instruction": system_instruction,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_tokens,
        }

    def query(
        self, prompt: str | Path, json_schema: str | Path, files: Iterable[str | Path]
    ) -> types.GenerateContentResponse:
        """Query the Gemini model with a given prompt and return the response.

        Parameters
        ----------
        prompt : str | Path
            The file to the prompt to send to the model.
        json_schema : str | Path | None
            The file to the JSON schema for the expected response format.
        files : Iterable[str | Path]
            A list of file paths to upload with the prompt.

        Returns
        -------
        response : types.GenerateContentResponse
            The response from the model.
        """
        prompt, files = super().query(prompt, files)

        # Add JSON schema for response, if provided
        if json_schema is not None:
            config = deepcopy(self._config)
            config["response_mime_type"] = "application/json"
            config["response_json_schema"] = read_json_schema(json_schema)
        else:
            config = self._config

        # Upload files and generate content
        uploaded_files = [self._client.files.upload(file=file) for file in files]
        response = self._client.models.generate_content(
            model=self._model_name,
            contents=[prompt, *uploaded_files],
            config=types.GenerateContentConfig(**config),
        )
        return response

    def close(self) -> None:
        """Close the model client."""
        self._client.close()

    def __del__(self) -> None:
        """Clean up resources when the model is deleted."""
        try:
            self.close()
        except Exception:
            pass
