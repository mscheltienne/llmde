from __future__ import annotations

import click

from .run_extraction import run as run_extraction
from .sys_info import run as sys_info


@click.group()
def run() -> None:
    """Main package entry-point."""  # noqa: D401


run.add_command(sys_info)
run.add_command(run_extraction)
