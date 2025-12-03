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
- **`intervention_protocol`**: Extracts intervention dosage and delivery parameters
  (intervention period, total sessions, total time, duration per session, game type, platform)
- **`outcome_assessment`**: Extracts primary outcomes targeted and assessment instruments used

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

## Command Line Interface

LLMDE provides two CLI commands: `prompt` for single queries and `run` for batch processing.

### API Key Configuration

Both `llmde prompt` and `llmde run` commands support two methods for providing API keys:

1. **Command line argument**: Use `--api-key "your-api-key"` with any command
2. **Environment variable**: Set the appropriate environment variable for your model:
   - For Claude models: `LLMDE_CLAUDE_API_KEY`
   - For Gemini models: `LLMDE_GEMINI_API_KEY`

**Example:**

```bash
# On Linux/macOS
export LLMDE_CLAUDE_API_KEY="sk-ant-api03-..."

# On Windows (PowerShell)
$env:LLMDE_CLAUDE_API_KEY="sk-ant-api03-..."

# On Windows (CMD)
set LLMDE_CLAUDE_API_KEY=sk-ant-api03-...

# Then run commands without --api-key
llmde prompt --model claude-sonnet-4-5-20250929 --prompt study_identifier --file paper.pdf
llmde run --src datasets --out results --model claude-sonnet-4-5-20250929 --prompts study_identifier
```

### Single Query: `llmde prompt`

Query a model with a prompt and files, returning the raw response.

#### Basic Usage

```bash
llmde prompt \
  --model <model_name> \
  --prompt <prompt_name> \
  --file <file1> [--file <file2> ...] \
  [--system-instruction <instruction_name>] \
  [--api-key <api_key>] \
  [--temperature <value>] \
  [--top-p <value>] \
  [--top-k <value>] \
  [--max-tokens <value>] \
  [--output <output_file>]
```

#### Required Arguments

- `--model`: Model to use (e.g., `claude-sonnet-4-5-20250929`, `gemini-2.0-flash`)
- `--prompt`: Prompt to use (built-in name or file path)
- `--file`: File to upload (can be specified multiple times)

#### Optional Arguments

- `--system-instruction`: System instruction (built-in name or file path)
- `--api-key`: API key for the model (if not provided, reads from environment variable)
- `--temperature`: Controls randomness in token selection, 0.0 to 1.0 (default: 0.0 for deterministic output)
- `--top-p`: Nucleus sampling threshold, 0.0 to 1.0 (default: unset, use API default)
- `--top-k`: Restricts sampling to top K tokens; use 1 for greedy decoding (default: unset)
- `--max-tokens`: Maximum tokens to generate (default: 4096)
- `--output`: Save response to file (if not provided, prints to stdout)

#### Examples

**Query with single PDF, print to stdout:**

```bash
llmde prompt \
  --model claude-sonnet-4-5-20250929 \
  --prompt study_identifier \
  --file paper.pdf
```

**Query with multiple PDFs, save to file:**

```bash
llmde prompt \
  --model claude-sonnet-4-5-20250929 \
  --prompt intervention_protocol \
  --file paper1.pdf --file paper2.pdf \
  --system-instruction systematic_review \
  --output results.txt
```

**Use custom prompt file:**

```bash
llmde prompt \
  --model gemini-2.0-flash \
  --prompt my_custom_prompt.md \
  --file paper.pdf \
  --output analysis.txt
```

#### Important Notes

- The `prompt` command returns the **raw response** from the model without any formatting
- No assumptions are made about JSON structure or output format
- This is ideal for exploratory queries, non-structured outputs, or custom use cases

### Batch Processing: `llmde run`

Process multiple PDF files with multiple prompts for structured data extraction.

#### Basic Usage

```bash
llmde run \
  --src <source_directory> \
  --out <output_directory> \
  --model <model_name> \
  --prompts <prompt_names> \
  [--system-instruction <instruction_name>] \
  [--api-key <api_key>] \
  [--temperature <value>] \
  [--top-p <value>] \
  [--top-k <value>] \
  [--max-tokens <value>]
```

#### Required Arguments

- `--src`: Source directory containing PDF files to analyze
- `--out`: Output directory for extraction results
- `--model`: Model to use (e.g., `claude-sonnet-4-5-20250929`, `gemini-2.0-flash`)
- `--prompts`: Comma-separated list of prompts (built-in names or file paths)

#### Optional Arguments

- `--system-instruction`: System instruction (built-in name or file path)
- `--api-key`: API key for the model (if not provided, reads from environment variable)
- `--temperature`: Controls randomness in token selection, 0.0 to 1.0 (default: 0.0 for deterministic output)
- `--top-p`: Nucleus sampling threshold, 0.0 to 1.0 (default: unset, use API default)
- `--top-k`: Restricts sampling to top K tokens; use 1 for greedy decoding (default: unset)
- `--max-tokens`: Maximum tokens to generate (default: 4096)

#### Examples

**Process PDFs with multiple prompts using Claude:**

```bash
llmde run \
  --src datasets \
  --out results \
  --model claude-sonnet-4-5-20250929 \
  --prompts study_identifier,study_information,intervention_protocol,outcome_assessment \
  --system-instruction systematic_review \
  --temperature 0.0 \
  --max-tokens 4096
```

**Using custom prompts:**

```bash
llmde run \
  --src datasets \
  --out results \
  --model gemini-2.0-flash \
  --prompts my_prompt.md,another_prompt.md \
  --system-instruction my_system.md
```

#### Output Structure

The CLI creates the following output structure:

```
output_directory/
├── MANIFEST.csv                    # Maps PDF names to numbered folders
├── 001/
│   ├── original_paper_name.pdf    # Copy of original PDF
│   ├── study_identifier.json      # Extracted data from first prompt
│   ├── study_information.json     # Extracted data from second prompt
│   └── ...                        # Additional prompts
├── 002/
│   └── ...
└── ...
```

**MANIFEST.csv** format:
```csv
index,pdf_name
001,Paper Title - Author - Year.pdf
002,Another Paper.pdf
...
```

#### Resume Capability

The CLI automatically skips already-processed files. If a JSON output file already
exists for a given PDF and prompt combination, it will not be re-extracted. This allows
you to:

- Resume interrupted extraction runs
- Add new papers to an existing output directory
- Re-run failed extractions by deleting only the failed JSON files
