[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/llmde/graph/badge.svg?token=pcLcPcQ4Ij)](https://codecov.io/gh/mscheltienne/llmde)
[![tests](https://github.com/mscheltienne/llmde/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/llmde/actions/workflows/pytest.yaml)

# LLMDE

WIP: LLM-based data extraction from scientific papers.

## Built-in Assets

The package includes built-in prompts and system instructions for common data extraction
tasks.

### Prompts

Prompts define the specific extraction task and output format. List and retrieve prompts
using the `prompts` module:

```python
from llmde.prompts import list_prompt_files, get_prompt

# List all available prompts
available_prompts = list_prompt_files()
print(available_prompts)  # ['study_identifier', ...]

# Get a specific prompt (returns markdown path and optional JSON schema path)
prompt_path, json_schema_path = get_prompt("study_identifier")
```

**Available Prompts:**

- **`study_identifier`**: Extracts bibliographic information (title, authors, year,
  journal, DOI) from scientific papers with source citations
- **`study_information`**: Extracts study methodology and demographics (completion status,
  country, study arms/conditions, participant age) with source citations

### System Instructions

System instructions provide high-level guidance to the model about its role and
behavior. Retrieve them similarly:

```python
from llmde.prompts import list_system_instruction, get_system_instruction

# List all available system instructions
available_instructions = list_system_instruction()
print(available_instructions)  # []

# Get a specific system instruction (returns markdown path)
system_path = get_system_instruction("name")
```

**Available System Instructions:**

- **`systematic_review`**: Persona for a researcher conducting systematic reviews of RCTs using gamified interventions (video games, serious games)

## Usage

### Gemini Backend

```python
from llmde.models import GeminiModel
from llmde.prompts import get_prompt, get_system_instruction
from llmde.io import read_markdown

# Get built-in prompt
prompt_path, json_schema_path = get_prompt("study_identifier")

# Optionally, get a system instruction
# system_path = get_system_instruction("name")
# system_instruction = read_markdown(system_path)

# Initialize model with deterministic parameters
api_key = ...
model = GeminiModel(
    "gemini-2.0-flash",
    api_key=api_key,
    temperature=0.0,
    top_k=1,
    top_p=0.0,
    # system_instruction=system_instruction,  # Optional
)

# Query with PDF files
response = model.query(prompt_path, json_schema_path, ["paper1.pdf", "paper2.pdf"])
print(response.text)
```

### Claude Backend

```python
from llmde.models import ClaudeModel
from llmde.prompts import get_prompt, get_system_instruction
from llmde.io import read_markdown

# Get built-in prompt (JSON schema not used by Claude)
prompt_path, _ = get_prompt("study_identifier")

# Optionally, get a system instruction
# system_path = get_system_instruction("name")
# system_instruction = read_markdown(system_path)

# Initialize model with deterministic parameters
api_key = ...
model = ClaudeModel(
    "claude-sonnet-4-5-20250929",  # or "claude-sonnet-4-5" for latest
    api_key=api_key,
    temperature=0.0,
    max_tokens=4096,
    # system_instruction=system_instruction,  # Optional
)

# Query with PDF files
response = model.query(prompt_path, ["paper1.pdf", "paper2.pdf"])
print(response)
```

### Using Custom Prompts

You can also provide your own prompt files:

```python
from pathlib import Path

# For Gemini (with JSON schema)
response = model.query(
    Path("my_prompt.md"),
    Path("my_schema.json"),
    ["paper.pdf"]
)

# For Claude (no JSON schema)
response = model.query(
    Path("my_prompt.md"),
    ["paper.pdf"]
)
```
