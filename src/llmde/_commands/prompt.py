from __future__ import annotations

from pathlib import Path

import click

from ..models import GeminiModel
from ..utils._checks import ensure_path
from ._utils import (
    get_api_key,
    get_model_class,
    get_prompt_path,
    get_system_instruction_text,
)


@click.command(name="prompt")
@click.option(
    "--model",
    required=True,
    type=str,
    help="Model to use (e.g., 'claude-sonnet-4-5-20250929', 'gemini-2.0-flash').",
)
@click.option(
    "--prompt",
    required=True,
    type=str,
    help="Prompt to use (built-in name or file path).",
)
@click.option(
    "--system-instruction",
    type=str,
    default=None,
    help="System instruction (built-in name or file path). Optional.",
)
@click.option(
    "--file",
    required=True,
    multiple=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="File to upload (PDFs). Can be specified multiple times.",
)
@click.option(
    "--api-key",
    type=str,
    default=None,
    help="API key for the model. If not provided, reads from environment variable.",
)
@click.option(
    "--temperature",
    type=float,
    default=0.0,
    help="Controls randomness in token selection (0.0 to 1.0). Use 0.0 for "
    "deterministic data extraction. Default: 0.0.",
)
@click.option(
    "--top-p",
    type=float,
    default=None,
    help="Nucleus sampling threshold (0.0 to 1.0). Lower values restrict sampling to "
    "higher-probability tokens. Leave unset when using temperature=0.0.",
)
@click.option(
    "--top-k",
    type=int,
    default=None,
    help="Restricts sampling to top K tokens. Use 1 for greedy decoding (maximum "
    "determinism). Leave unset for API default.",
)
@click.option(
    "--max-tokens",
    type=int,
    default=8192,
    help="Maximum tokens to generate. Set high enough for expected JSON output size. "
    "Default: 8192.",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file path to save response (optional). If not provided, prints to "
    "stdout.",
)
def run(
    model: str,
    prompt: str,
    file: tuple[Path, ...],
    system_instruction: str | None,
    api_key: str | None,
    temperature: float,
    top_p: float | None,
    top_k: int | None,
    max_tokens: int,
    output: Path | None,
) -> None:
    """Query a model with a prompt and files.

    This command allows you to query a language model with a specific prompt and
    upload files (PDFs) for analysis. The response is either printed to stdout or
    saved to a file.
    """
    header = "LLMDE Prompt Query"
    click.echo("=" * len(header))
    click.echo(header)
    click.echo("=" * len(header))

    # Get prompt
    click.echo(f"\nLoading prompt: {prompt}")
    prompt_path, json_schema_path = get_prompt_path(prompt)
    schema_info = " (with JSON schema)" if json_schema_path else ""
    click.echo(f"  ✓ Prompt loaded: {prompt_path}{schema_info}")

    # Get system instruction
    system_text = None
    if system_instruction is not None:
        click.echo(f"\nLoading system instruction: {system_instruction}")
        system_text = get_system_instruction_text(system_instruction)
        click.echo("  ✓ Loaded")

    # Get API key
    click.echo("\nRetrieving API key...")
    api_key_value = get_api_key(model, api_key)
    click.echo("  ✓ API key retrieved")

    # Validate files
    click.echo(f"\nValidating {len(file)} file(s)...")
    for file_path in file:
        file_path = ensure_path(file_path, must_exist=True)
        click.echo(f"  ✓ {file_path.name}")

    # Initialize model
    click.echo(f"\nInitializing model: {model}")
    model_class = get_model_class(model)

    # Build model kwargs
    model_kwargs = {
        "model_name": model,
        "api_key": api_key_value,
        "system_instruction": system_text,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_tokens": max_tokens,
    }

    model_instance = model_class(**model_kwargs)
    click.echo("  ✓ Model initialized")

    # Query model
    click.echo("\n📝 Querying model...")
    try:
        if isinstance(model_instance, GeminiModel):
            response = model_instance.query(prompt_path, json_schema_path, file)
            # GeminiModel returns GenerateContentResponse object
            response_text = response.text
        else:  # ClaudeModel or others
            response_text = model_instance.query(prompt_path, file)

        click.echo("  ✓ Response received")

        # Output response
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as fid:
                fid.write(response_text)
            click.echo(f"\n✓ Response saved to: {output}")
        else:
            header = "Model Response"
            click.echo("\n" + "=" * len(header))
            click.echo(header)
            click.echo("=" * len(header))
            click.echo(response_text)

    except Exception as exc:
        click.echo(f"    ✗ Error: {exc}")
    finally:
        # Cleanup
        model_instance.close()
