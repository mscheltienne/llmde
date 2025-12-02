"""Command to launch the LLMDE GUI."""

from __future__ import annotations

import sys

import click

from .._gui import run_gui


@click.command(name="gui")
def run() -> None:
    """Launch the LLMDE graphical user interface."""
    sys.exit(run_gui())
