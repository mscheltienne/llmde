from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from anthropic import Anthropic

from ..io import read_prompt
from ..utils._checks import check_type, ensure_path
from ._base import BaseModel

if TYPE_CHECKING:
    from pathlib import Path


class ClaudeModel(BaseModel):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        *,
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int = 4096,
    ) -> None:
        """Initialize the Claude model with the given model name and API key.

        Parameters
        ----------
        model_name : str
            The name of the Claude model to use (e.g., ``"claude-sonnet-4-5"`` or
            ``"claude-sonnet-4-5-20250929"`` for specific versions).
        api_key : str
            The API key for accessing the Claude API.
        system : str | None
            System prompt to provide context and instructions to the model.
        temperature : float | None
            Amount of randomness in the response. Ranges from ``0.0`` to ``1.0``.
            Use lower values (e.g., ``0.0``) for more deterministic, focused outputs,
            and higher values (e.g., ``1.0``) for more creative, diverse outputs.
        max_tokens : int
            Maximum number of tokens to generate in the response. This is a required
            parameter for Claude API. Default is 4096.

        Notes
        -----
        Unlike other LLM APIs, Claude does not support ``top_k`` or ``top_p``
        parameters. For deterministic outputs in data extraction tasks, use
        ``temperature=0.0``.

        Note that even with ``temperature=0.0``, the results will not be fully
        deterministic due to implementation details in GPU operations.

        See https://docs.anthropic.com/en/api/messages for more information.
        """  # noqa: E501
        check_type(model_name, (str,), "model_name")
        check_type(api_key, (str,), "api_key")
        self._client = Anthropic(api_key=api_key)
        self._model_name = model_name
        check_type(system, (str, None), "system")
        check_type(temperature, ("numeric", None), "temperature")
        if temperature is not None and (temperature < 0.0 or temperature > 1.0):
            raise ValueError(
                f"Temperature must be between 0.0 and 1.0. Provided {temperature} is "
                "invalid."
            )
        check_type(max_tokens, ("int-like",), "max_tokens")
        self._system = system
        self._temperature = temperature
        self._max_tokens = max_tokens

    def query(self, prompt: str | Path, files: Iterable[str | Path]) -> str:
        """Query the Claude model with a given prompt and return the response.

        Parameters
        ----------
        prompt : str | Path
            The path to the prompt file to send to the model.
        files : Iterable[str | Path]
            A list of file paths (PDFs) to upload and analyze with the prompt.

        Returns
        -------
        response : str
            The text response from the model.

        Notes
        -----
        This method uses Claude's Files API to upload documents.
        """
        prompt_text = read_prompt(prompt)
        check_type(files, (Iterable,), "files")
        files = [ensure_path(file, must_exist=True) for file in files]

        # Upload files using the Files API
        uploaded_file_ids = []
        for file_path in files:
            with open(file_path, "rb") as fid:
                uploaded_file = self._client.beta.files.upload(
                    file=(file_path.name, fid, "application/pdf")
                )
            uploaded_file_ids.append(uploaded_file.id)

        # Build message content with uploaded files
        message_content = [
            {
                "type": "document",
                "source": {
                    "type": "file",
                    "file_id": file_id,
                },
            }
            for file_id in uploaded_file_ids
        ]
        message_content.append({"type": "text", "text": prompt_text})

        # Create message with appropriate parameters
        kwargs = {
            "model": self._model_name,
            "max_tokens": self._max_tokens,
            "messages": [{"role": "user", "content": message_content}],
        }

        if self._system is not None:
            kwargs["system"] = self._system
        if self._temperature is not None:
            kwargs["temperature"] = self._temperature

        # Make API call with Files API beta flag
        response = self._client.beta.messages.create(
            **kwargs,
            betas=["files-api-2025-04-14"],
        )

        # Extract text response
        for content_block in response.content:
            if content_block.type == "text":
                return content_block.text
        raise ValueError("No text content found in response")

    def close(self) -> None:
        """Close the model client."""
        self._client.close()

    def __del__(self) -> None:
        """Clean up resources when the model is deleted."""
        try:
            self.close()
        except Exception:
            pass
