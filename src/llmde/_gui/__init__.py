"""LLMDE GUI module.

This module provides a PyQt6-based graphical user interface for the LLMDE
data extraction tool.
"""

from __future__ import annotations

from .main import MainWindow, run_gui

__all__: list[str] = ["MainWindow", "run_gui"]
