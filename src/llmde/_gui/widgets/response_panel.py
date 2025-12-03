"""Response display panel with copy functionality."""

from __future__ import annotations

import re

import qtawesome as qta
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from superqt.utils import CodeSyntaxHighlight

from ..utils import GUIConfig


class ResponsePanel(QWidget):
    """Panel for displaying LLM responses with copy functionality.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Displays responses in a read-only text area with JSON syntax highlighting.
    Includes a copy button to copy the response to clipboard.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._highlighter: CodeSyntaxHighlight | None = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Header with label and copy button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel("Response")
        self._label.setProperty("class", "section-header")
        header_layout.addWidget(self._label)

        header_layout.addStretch()

        # Copy button
        self._copy_btn = QPushButton()
        self._copy_btn.setFixedSize(32, 32)
        self._copy_btn.setToolTip("Copy response to clipboard")
        self._copy_btn.setEnabled(False)
        copy_icon = qta.icon(
            GUIConfig.ICONS["copy"], color=GUIConfig.COLORS["text_secondary"]
        )
        self._copy_btn.setIcon(copy_icon)
        self._copy_btn.clicked.connect(self._copy_to_clipboard)
        header_layout.addWidget(self._copy_btn)

        layout.addLayout(header_layout)

        # Response text area
        self._text_edit = QPlainTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setPlaceholderText("Response will appear here...")

        # Set monospace font
        font = QFont("Consolas", 11)
        self._text_edit.setFont(font)

        # Apply dark theme styling for response area
        self._text_edit.setStyleSheet(
            f"""
            QPlainTextEdit {{
                background-color: {GUIConfig.COLORS["response_bg"]};
                color: {GUIConfig.COLORS["response_text"]};
                border: 1px solid {GUIConfig.COLORS["border_primary"]};
                border-radius: 4px;
                padding: 10px;
            }}
            """
        )

        # Set minimum height
        self._text_edit.setMinimumHeight(200)

        layout.addWidget(self._text_edit, 1)

    def set_response(self, text: str) -> None:
        """Set the response text.

        Parameters
        ----------
        text : str
            The response text to display.
        """
        # Strip markdown code fences if present
        text = self._strip_code_fences(text)

        self._text_edit.setPlainText(text)
        self._copy_btn.setEnabled(bool(text.strip()))

        # Apply JSON highlighting if content looks like JSON
        if text.strip().startswith("{") or text.strip().startswith("["):
            if self._highlighter is None:
                self._highlighter = CodeSyntaxHighlight(
                    self._text_edit.document(), "json", "github-dark"
                )
            self._highlighter.rehighlight()
        else:
            # Remove highlighter for non-JSON content
            if self._highlighter is not None:
                self._highlighter.setDocument(None)
                self._highlighter = None

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        """Strip markdown code fences from text.

        Parameters
        ----------
        text : str
            The text potentially wrapped in code fences.

        Returns
        -------
        str
            The text with code fences removed.
        """
        # Pattern matches ```json or ``` at start, and ``` at end
        pattern = r"^```(?:json)?\s*\n?(.*?)\n?```\s*$"
        match = re.match(pattern, text.strip(), re.DOTALL)
        if match:
            return match.group(1).strip()
        return text

    def get_response(self) -> str:
        """Get the current response text.

        Returns
        -------
        str
            The response text.
        """
        return self._text_edit.toPlainText()

    def clear(self) -> None:
        """Clear the response text."""
        self._text_edit.clear()
        self._copy_btn.setEnabled(False)

        # Remove highlighter
        if self._highlighter is not None:
            self._highlighter.setDocument(None)
            self._highlighter = None

    def _copy_to_clipboard(self) -> None:
        """Copy the response text to clipboard."""
        text = self._text_edit.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

            # Visual feedback - temporarily change button icon
            success_icon = qta.icon(
                GUIConfig.ICONS["valid"], color=GUIConfig.COLORS["validation_success"]
            )
            self._copy_btn.setIcon(success_icon)
            self._copy_btn.setToolTip("Copied!")

            # Restore original icon after delay
            QTimer.singleShot(1500, self._restore_copy_icon)

    def _restore_copy_icon(self) -> None:
        """Restore the copy button icon to its original state."""
        copy_icon = qta.icon(
            GUIConfig.ICONS["copy"], color=GUIConfig.COLORS["text_secondary"]
        )
        self._copy_btn.setIcon(copy_icon)
        self._copy_btn.setToolTip("Copy response to clipboard")

    def set_loading(self, loading: bool) -> None:
        """Set the loading state.

        Parameters
        ----------
        loading : bool
            Whether to show loading state.
        """
        if loading:
            self._text_edit.setPlaceholderText("Waiting for response...")
            self._copy_btn.setEnabled(False)
        else:
            self._text_edit.setPlaceholderText("Response will appear here...")

    def is_empty(self) -> bool:
        """Check if the response is empty.

        Returns
        -------
        bool
            True if no response text.
        """
        return not self._text_edit.toPlainText().strip()
