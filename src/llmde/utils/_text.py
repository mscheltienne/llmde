"""Text processing utilities."""

from __future__ import annotations

import re


def strip_markdown_fences(text: str) -> str:
    r"""Strip markdown code fences from text.

    Parameters
    ----------
    text : str
        The text potentially wrapped in code fences, e.g.::

            ```json
            {"key": "value"}
            ```

    Returns
    -------
    str
        The text with code fences removed. If no fences are present,
        the original text is returned unchanged.

    Examples
    --------
    >>> strip_markdown_fences('```json\\n{"key": "value"}\\n```')
    '{"key": "value"}'
    >>> strip_markdown_fences('{"key": "value"}')
    '{"key": "value"}'
    """
    # Pattern matches ```json or ``` at start, and ``` at end
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```\s*$"
    match = re.match(pattern, text.strip(), re.DOTALL)
    if match:
        return match.group(1).strip()
    return text
