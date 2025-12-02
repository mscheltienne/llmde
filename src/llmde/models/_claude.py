from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from anthropic import Anthropic

from ._base import BaseModel

if TYPE_CHECKING:
    from pathlib import Path


class ClaudeModel(BaseModel):
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
        """Initialize the Claude model with the given model name and API key.

        Parameters
        ----------
        model_name : str
            The name of the Claude model to use (e.g., ``"claude-sonnet-4-5"`` or
            ``"claude-sonnet-4-5-20250929"`` for a specific version).
        api_key : str
            The API key for accessing the Claude API.
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
            Maximum number of tokens to generate in the response. This is a required
            parameter for Claude API. Defaults to ``4096``. Set this high enough to
            accommodate the expected JSON output size for data extraction tasks.

        Notes
        -----
        **Claude-specific considerations:**

        - Anthropic recommends adjusting ``temperature`` first. Only modify ``top_p``
          or ``top_k`` for advanced use cases.
        - Anthropic suggests using either ``temperature`` or ``top_p``, not both
          simultaneously for fine-tuned control.
        - Even with ``temperature=0.0``, outputs may not be fully deterministic.

        **Recommended settings for deterministic data extraction:**

        - ``temperature=0.0``: Primary parameter for deterministic outputs.
        - ``top_k=1``: Greedy decoding for maximum determinism.
        - ``top_p``: Leave as ``None`` when using ``temperature=0.0``.

        See https://docs.anthropic.com/en/api/messages for API documentation and
        https://towardsdatascience.com/how-to-write-expert-prompts-for-chatgpt-gpt-4-and-other-language-models-23133dc85550/
        for prompt engineering tips and best practices.
        """
        super().__init__(
            model_name,
            api_key,
            system_instruction=system_instruction,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
        )
        self._client = Anthropic(api_key=api_key)

        # Create Claude-specific config dictionary
        # Note: Claude API uses "system" instead of "system_instruction"
        self._config = {
            "model": model_name,
            "system": system_instruction,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_tokens": max_tokens,
        }

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
        prompt, files = super().query(prompt, files)

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
        message_content.append({"type": "text", "text": prompt})

        # Create message with appropriate parameters
        # Note: Claude uses a built-in "omit" system instead of `None`, thus we filter
        # out None values from config before passing to API.
        kwargs = {k: v for k, v in self._config.items() if v is not None}
        kwargs["messages"] = [{"role": "user", "content": message_content}]

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
