[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/llmde/graph/badge.svg?token=pcLcPcQ4Ij)](https://codecov.io/gh/mscheltienne/llmde)
[![tests](https://github.com/mscheltienne/llmde/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/llmde/actions/workflows/pytest.yaml)

# LLMDE

WIP: LLM-based data extraction from scientific papers.

## Usage

### Gemini Backend

```python
from llmde.models import GeminiModel

api_key = ...
model = GeminiModel(
    "gemini-2.0-flash",
    api_key=api_key,
    temperature=0.0,
    top_k=1,
    top_p=0.0,
)
response = model.query(path_to_prompt, path_to_json_schema, [path_to_file1, path_to_file2])
```

### Claude Backend

```python
from llmde.models import ClaudeModel

api_key = ...
model = ClaudeModel(
    "claude-sonnet-4-5-20250929",  # or "claude-sonnet-4-5" for latest
    api_key=api_key,
    temperature=0.0,
    max_tokens=4096,
)
response = model.query(path_to_prompt, [path_to_file1, path_to_file2])
```
