from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import TYPE_CHECKING

from google import genai
from google.genai import types

from ..io import read_json_schema, read_prompt
from ..utils._checks import check_type, ensure_path
from ._base import BaseModel

if TYPE_CHECKING:
    from pathlib import Path


class GeminiModel(BaseModel):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        *,
        system_instruction: types.ContentUnion | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: float | None = None,
        max_output_tokens: int | None,
    ) -> None:
        """Initialize the Gemini model with the given model name and API key.

        Parameters
        ----------
        model_name : str
            The name of the Gemini model to use.
        api_key : str
            The API key for accessing the Gemini model.
        system_instruction : str | None
            Instructions for the model to steer it toward better performance.
            For example, ``"Answer as concisely as possible"`` or ``"Don't use technical
            terms in your response"``.
        temperature : float | None
            Value that controls the degree of randomness in token selection.
            Lower temperatures are good for prompts that require a less open-ended or
            creative response, while higher temperatures can lead to more diverse or
            creative results. Ranges from ``0.0`` to ``1.0``.
        top_p : float | None
            Tokens are selected from the most to least probable until the sum
            of their probabilities equals this value. Use a lower value for less
            random responses and a higher value for more random responses.
        top_k : float | None
            For each token selection step, the ``top_k`` tokens with the
            highest probabilities are sampled. Then tokens are further filtered based
            on ``top_p`` with the final token selected using temperature sampling. Use
            a lower number for less random responses and a higher number for more
            random responses.
        max_output_tokens : int | None
            Maximum number of tokens that can be generated in the response.

        Notes
        -----
        See https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values
        for information about the parameters. Recommended values are:

        - ``temperature``: 0 or very low
        - ``top_p``: 0 or very low
        - ``top_k``: 1 or very low (minimum 1)
        """  # noqa: E501
        check_type(model_name, (str,), "model_name")
        check_type(api_key, (str,), "api_key")
        self._client = genai.Client(
            api_key=api_key, http_options=types.HttpOptions(api_version="v1")
        )
        self._model_name = model_name
        check_type(
            system_instruction, (str, types.ContentUnion, None), "system_instruction"
        )
        check_type(temperature, ("numeric", None), "temperature")
        if temperature is not None and (temperature < 0.0 or temperature > 1.0):
            raise ValueError(
                f"Temperature must be between 0.0 and 1.0. Provided {temperature} is "
                "invalid."
            )
        check_type(top_p, ("numeric", None), "top_p")
        check_type(top_k, ("numeric", None), "top_k")
        check_type(max_output_tokens, ("numeric", None), "max_output_tokens")
        self._config = {
            "system_instruction": system_instruction,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
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
        prompt = read_prompt(prompt)
        check_type(files, (Iterable,), "files")
        files = [ensure_path(file, must_exist=True) for file in files]

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
