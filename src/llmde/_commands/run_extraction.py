from __future__ import annotations

import csv
import json
import shutil
import time
from pathlib import Path

import click

from ..models import GeminiModel
from ._utils import (
    get_api_key,
    get_model_class,
    get_prompt_path,
    get_system_instruction_text,
)


def _parse_prompts(prompts_str: str) -> list[tuple[Path, Path | None]]:
    """Parse comma-separated prompt list into paths.

    Parameters
    ----------
    prompts_str : str
        Comma-separated list of prompt names or paths.

    Returns
    -------
    list of tuple of (Path, Path | None)
        List of tuples (prompt_path, json_schema_path).

    Raises
    ------
    ValueError
        If a prompt name is not found in built-in prompts.
    """
    prompt_data = []

    for prompt_name in [prompt.strip() for prompt in prompts_str.split(",")]:
        prompt_path, json_schema_path = get_prompt_path(prompt_name)
        prompt_data.append((prompt_path, json_schema_path))

    return prompt_data


def _strip_markdown_fences(response: str) -> str:
    """Strip markdown code fences from response text.

    Parameters
    ----------
    response : str
        Raw response text that may contain markdown code fences.

    Returns
    -------
    str
        Cleaned response text with code fences removed.

    Notes
    -----
    This function removes common markdown code fence patterns like ```json or ```
    from the beginning and end of the response text.
    """
    response_clean = response.strip()
    if response_clean.startswith("```json"):
        response_clean = response_clean[7:]
    elif response_clean.startswith("```"):
        response_clean = response_clean[3:]
    if response_clean.endswith("```"):
        response_clean = response_clean[:-3]
    return response_clean.strip()


@click.command(name="run")
@click.option(
    "--src",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Source directory containing PDF files to analyze.",
)
@click.option(
    "--out",
    required=True,
    type=click.Path(path_type=Path),
    help="Output directory for extraction results.",
)
@click.option(
    "--model",
    required=True,
    type=str,
    help="Model to use (e.g., 'claude-sonnet-4-5-20250929', 'gemini-2.0-flash').",
)
@click.option(
    "--prompts",
    "prompts",
    required=True,
    type=str,
    help="Comma-separated list of prompts (built-in names or file paths).",
)
@click.option(
    "--system-instruction",
    type=str,
    default=None,
    help="System instruction (built-in name or file path). Optional.",
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
    default=4096,
    help="Maximum tokens to generate. Set high enough for expected JSON output size. "
    "Default: 4096.",
)
def run(
    src: Path,
    out: Path,
    model: str,
    prompts: str,
    system_instruction: str | None,
    api_key: str | None,
    temperature: float,
    top_p: float | None,
    top_k: int | None,
    max_tokens: int,
) -> None:
    """Run data extraction pipeline on PDF files.

    Extracts structured information from scientific papers using LLMs.
    """
    header = "LLMDE Data Extraction Pipeline"
    click.echo("=" * len(header))
    click.echo(header)
    click.echo("=" * len(header))

    # Parse prompts
    click.echo("\nParsing prompts...")
    prompt_data = _parse_prompts(prompts)
    for i, (prompt_path, json_schema_path) in enumerate(prompt_data, 1):
        schema_info = " (with JSON schema)" if json_schema_path else ""
        click.echo(f"  {i}. {prompt_path.stem}: {prompt_path}{schema_info}")

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

    # Get list of PDFs
    pdf_files = sorted(src.glob("*.pdf"))
    if not pdf_files:
        click.echo(f"\n✗ No PDF files found in {src}")
        return

    click.echo(f"\nFound {len(pdf_files)} PDF files to process")

    # Create output directory
    out.mkdir(parents=True, exist_ok=True)
    click.echo(f"Output directory: {out}\n")

    # Prepare manifest
    manifest_path = out / "MANIFEST.csv"
    manifest_data = []

    # Process each PDF
    for pdf_idx, pdf_path in enumerate(pdf_files, 1):
        click.echo(f"\n[{pdf_idx}/{len(pdf_files)}] Processing: {pdf_path.name}")
        click.echo("-" * 80)

        # Create numbered output directory
        pdf_output_dir = out / f"{pdf_idx:03d}"
        pdf_output_dir.mkdir(parents=True, exist_ok=True)

        # Copy PDF with original name
        output_pdf_path = pdf_output_dir / pdf_path.name
        if not output_pdf_path.exists():
            shutil.copy2(pdf_path, output_pdf_path)
            click.echo(f"✓ PDF copied: {pdf_path.name}")
        else:
            click.echo(f"⊘ PDF exists: {pdf_path.name}")

        # Add to manifest
        manifest_data.append({"index": f"{pdf_idx:03d}", "pdf_name": pdf_path.name})

        # Process each prompt
        for prompt_idx, (prompt_path, json_schema_path) in enumerate(prompt_data, 1):
            prompt_name = prompt_path.stem
            click.echo(f"\n  [{prompt_idx}/{len(prompt_data)}] {prompt_name}")

            output_json_path = pdf_output_dir / f"{prompt_name}.json"

            # Skip if already processed
            if output_json_path.exists():
                click.echo("    ⊘ Already exists, skipping")
                continue

            try:
                # Query model (different signatures for different models)
                click.echo("    📝 Querying model...")
                if isinstance(model_instance, GeminiModel):
                    response = model_instance.query(
                        prompt_path, [pdf_path], json_schema_path
                    )
                else:  # ClaudeModel or others
                    response = model_instance.query(prompt_path, [pdf_path])

                # Strip markdown code fences if present
                response_clean = _strip_markdown_fences(response)

                # Parse and save
                try:
                    response_data = json.loads(response_clean)
                    with open(output_json_path, "w", encoding="utf-8") as f:
                        json.dump(response_data, f, indent=2, ensure_ascii=False)
                    click.echo(f"    ✓ Saved valid JSON: {prompt_name}.json")
                except json.JSONDecodeError as exc:
                    click.echo(f"    ⚠ Invalid JSON ({exc}), saving raw text")
                    with open(output_json_path, "w", encoding="utf-8") as f:
                        f.write(response)

            except Exception as exc:
                click.echo(f"    ✗ Error: {exc}")

            time.sleep(30)  # to avod rate limits
        time.sleep(30)  # to avoid rate limits

    # Write manifest
    click.echo(f"\nWriting manifest: {manifest_path}")
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "pdf_name"])
        writer.writeheader()
        writer.writerows(manifest_data)

    # Summary
    click.echo("✓ Extraction complete!")
    click.echo(f"✓ Processed {len(pdf_files)} papers")
    click.echo(f"✓ Results: {out}")

    # Cleanup
    model_instance.close()
