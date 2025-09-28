[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/llmde/graph/badge.svg?token=pcLcPcQ4Ij)](https://codecov.io/gh/mscheltienne/llmde)
[![tests](https://github.com/mscheltienne/llmde/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/llmde/actions/workflows/pytest.yaml)

# LLMDE

WIP: LLM-based data extraction from scientific papers.

## Usage

```python
from llmde.models import GeminiModel

api_key = ...
model = GeminiModel("gemini-2.5-flash", api_key=api_key, temperature=0.1)
model.query(path_to_prompt, path_to_json_schema, [path_to_file1, path_to_file2])
```
