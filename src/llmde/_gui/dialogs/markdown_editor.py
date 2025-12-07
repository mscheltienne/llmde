"""Markdown editor dialog for viewing and editing prompts."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from superqt.utils import CodeSyntaxHighlight

from ..widgets.line_number_edit import LineNumberTextEdit

if TYPE_CHECKING:
    from PyQt6.QtGui import QCloseEvent


class MarkdownEditorDialog(QDialog):
    """Dialog for viewing and editing markdown prompt files.

    Parameters
    ----------
    file_path : str
        Path to the markdown file to edit.
    is_builtin : bool
        Whether this is a built-in prompt (read-only).
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Built-in prompts are displayed in read-only mode with save disabled.
    Custom prompts can be edited and saved.
    """

    def __init__(
        self,
        file_path: str,
        is_builtin: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._file_path = Path(file_path)
        self._is_builtin = is_builtin
        self._original_content = ""
        self._has_changes = False
        self._highlighter: CodeSyntaxHighlight | None = None

        self._setup_ui()
        self._load_content()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle(f"Edit: {self._file_path.name}")
        self.setMinimumSize(700, 500)
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Header with file path
        header_layout = QHBoxLayout()
        self._path_label = QLabel(str(self._file_path))
        self._path_label.setProperty("class", "editor-path")
        self._path_label.setWordWrap(True)
        header_layout.addWidget(self._path_label, 1)
        layout.addLayout(header_layout)

        # Read-only warning banner for built-in prompts
        if self._is_builtin:
            self._warning_banner = QLabel(
                "This is a built-in prompt and cannot be modified."
            )
            self._warning_banner.setProperty("class", "warning-banner")
            self._warning_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self._warning_banner)

        # Text editor with line numbers
        self._editor = LineNumberTextEdit()
        self._editor.setReadOnly(self._is_builtin)

        # Apply markdown highlighting
        self._highlighter = CodeSyntaxHighlight(
            self._editor.document(), "markdown", "default"
        )

        layout.addWidget(self._editor, 1)

        # Button row
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Cancel button
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setFixedWidth(100)
        self._cancel_btn.clicked.connect(self._on_cancel)
        button_layout.addWidget(self._cancel_btn)

        # Save button
        self._save_btn = QPushButton("Save")
        self._save_btn.setFixedWidth(100)
        self._save_btn.setEnabled(False)
        self._save_btn.setProperty("class", "action-button")
        self._save_btn.clicked.connect(self._on_save)
        button_layout.addWidget(self._save_btn)

        layout.addLayout(button_layout)

    def _load_content(self) -> None:
        """Load content from the file."""
        try:
            self._original_content = self._file_path.read_text(encoding="utf-8")
            self._editor.setPlainText(self._original_content)
        except FileNotFoundError:
            self._editor.setPlainText("")
            self._original_content = ""
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load file: {e}",
            )
            self._editor.setPlainText("")
            self._original_content = ""

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        if not self._is_builtin:
            self._editor.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self) -> None:
        """Handle text changes in the editor."""
        current_content = self._editor.toPlainText()
        self._has_changes = current_content != self._original_content
        self._save_btn.setEnabled(self._has_changes)

    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        if self._has_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to close?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.reject()

    def _on_save(self) -> None:
        """Handle save button click."""
        if self._is_builtin:
            QMessageBox.warning(
                self,
                "Cannot Save",
                "Built-in prompts cannot be modified.",
            )
            return

        try:
            content = self._editor.toPlainText()
            self._file_path.write_text(content, encoding="utf-8")
            self._original_content = content
            self._has_changes = False
            self._save_btn.setEnabled(False)

            QMessageBox.information(
                self,
                "Saved",
                f"File saved successfully:\n{self._file_path}",
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to save file: {exc}")

    def get_content(self) -> str:
        """Get the current editor content.

        Returns
        -------
        str
            The editor content.
        """
        return self._editor.toPlainText()

    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes.

        Returns
        -------
        bool
            True if there are unsaved changes.
        """
        return self._has_changes

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event.

        Parameters
        ----------
        event : QCloseEvent
            The close event.
        """
        if self._has_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Are you sure you want to close?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        event.accept()
