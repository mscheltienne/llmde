"""Prompt and system instruction selector widget."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import qtawesome as qta
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from llmde.prompts import (
    get_prompt,
    get_system_instruction,
    list_prompt_files,
    list_system_instruction,
)

from ..utils import GUIConfig, set_validation_icon


class PromptSelectorWidget(QWidget):
    """Widget for selecting prompts or system instructions.

    Parameters
    ----------
    selector_type : str
        The type of selector: 'prompt' or 'system'.
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Supports selection of built-in prompts by name or custom file paths.
    Includes an EDIT button to open the markdown editor.
    """

    selectionChanged = pyqtSignal(str, bool)  # (value, is_builtin)
    editRequested = pyqtSignal(str, bool)  # (path_or_name, is_builtin)
    validationChanged = pyqtSignal(bool)

    # Special items in combo box
    SEPARATOR = "---"
    NONE_ITEM = "(None)"
    BROWSE_ITEM = "Browse for file..."

    def __init__(
        self,
        selector_type: Literal["prompt", "system"],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        if selector_type not in ("prompt", "system"):
            raise ValueError("selector_type must be 'prompt' or 'system'")
        self._selector_type = selector_type
        self._is_valid = selector_type == "system"  # System is optional
        self._current_value: str | None = None
        self._is_builtin = True
        self._custom_path: str | None = None
        self._has_json_schema = False

        self._setup_ui()
        self._populate_combo()
        self._connect_signals()
        # Trigger initial validation for the pre-selected item
        self._on_combo_changed(self._combo.currentText())

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        label_text = (
            "System Instruction:" if self._selector_type == "system" else "Prompt:"
        )
        self._label = QLabel(label_text)
        self._label.setFixedWidth(120)
        layout.addWidget(self._label)

        # Combo box for selection
        self._combo = QComboBox()
        self._combo.setMinimumWidth(200)
        layout.addWidget(self._combo, 1)

        # JSON schema indicator (only for prompts)
        if self._selector_type == "prompt":
            self._json_indicator = QLabel()
            self._json_indicator.setFixedSize(20, 20)
            self._json_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._json_indicator.setToolTip("JSON schema status")
            layout.addWidget(self._json_indicator)
            self._update_json_indicator()

        # Validation icon
        self._validation_icon = QLabel()
        self._validation_icon.setFixedSize(*GUIConfig.VALIDATION_ICON_SIZE)
        self._validation_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._validation_icon)

        # Edit button
        self._edit_btn = QPushButton("Edit")
        self._edit_btn.setFixedWidth(60)
        self._edit_btn.setToolTip("Edit the selected prompt/instruction")
        layout.addWidget(self._edit_btn)

        self._update_validation()

    def _populate_combo(self) -> None:
        """Populate the combo box with built-in options."""
        self._combo.clear()

        if self._selector_type == "system":
            # Add None option for system instructions (optional)
            self._combo.addItem(self.NONE_ITEM)
            self._combo.insertSeparator(1)

            # Add built-in system instructions
            builtins = list_system_instruction()
            for name in sorted(builtins):
                self._combo.addItem(name)
        else:
            # Add built-in prompts
            builtins = list_prompt_files()
            for name in sorted(builtins):
                self._combo.addItem(name)

        # Add separator and browse option
        self._combo.insertSeparator(self._combo.count())
        self._combo.addItem(self.BROWSE_ITEM)

        # Set default selection
        self._combo.setCurrentIndex(0)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._combo.currentTextChanged.connect(self._on_combo_changed)
        self._edit_btn.clicked.connect(self._on_edit_clicked)

    def _on_combo_changed(self, text: str) -> None:
        """Handle combo box selection changes.

        Parameters
        ----------
        text : str
            The selected text.
        """
        if text == self.BROWSE_ITEM:
            self._browse_for_file()
            return

        if text == self.NONE_ITEM:
            self._current_value = None
            self._is_builtin = True
            self._has_json_schema = False
            self._custom_path = None
        elif Path(text).is_absolute():
            # This is a custom path
            self._current_value = text
            self._is_builtin = False
            self._custom_path = text
            self._check_json_schema_for_custom()
        else:
            # Built-in prompt
            self._current_value = text
            self._is_builtin = True
            self._custom_path = None
            self._check_json_schema_for_builtin()

        self._update_validation()
        self._update_json_indicator()
        self.selectionChanged.emit(self._current_value or "", self._is_builtin)

    def _browse_for_file(self) -> None:
        """Open file dialog to browse for a custom prompt file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Prompt File",
            "",
            "Markdown Files (*.md);;All Files (*)",
        )

        if file_path:
            # Add to combo if not already present
            index = self._combo.findText(file_path)
            if index == -1:
                # Insert before the separator (before Browse option)
                insert_pos = self._combo.count() - 2
                self._combo.insertItem(insert_pos, file_path)
                self._combo.setCurrentIndex(insert_pos)
            else:
                self._combo.setCurrentIndex(index)
        else:
            # User cancelled, revert to previous selection
            if self._current_value:
                index = self._combo.findText(self._current_value)
                if index >= 0:
                    self._combo.setCurrentIndex(index)

    def _check_json_schema_for_builtin(self) -> None:
        """Check if built-in prompt has a JSON schema."""
        if self._selector_type != "prompt" or not self._current_value:
            self._has_json_schema = False
            return

        try:
            _, json_path = get_prompt(self._current_value)
            self._has_json_schema = json_path is not None
        except Exception:
            self._has_json_schema = False

    def _check_json_schema_for_custom(self) -> None:
        """Check if custom prompt has a JSON schema file."""
        if self._selector_type != "prompt" or not self._custom_path:
            self._has_json_schema = False
            return

        # Check for JSON file with same name
        prompt_path = Path(self._custom_path)
        json_path = prompt_path.with_suffix(".json")
        self._has_json_schema = json_path.exists()

    def _update_json_indicator(self) -> None:
        """Update the JSON schema indicator icon."""
        if self._selector_type != "prompt":
            return

        if self._has_json_schema:
            icon = qta.icon(
                GUIConfig.ICONS["json"], color=GUIConfig.COLORS["accent_primary"]
            )
            self._json_indicator.setPixmap(icon.pixmap(16, 16))
            self._json_indicator.setToolTip("JSON schema attached")
        else:
            icon = qta.icon(
                GUIConfig.ICONS["json"], color=GUIConfig.COLORS["text_muted"]
            )
            self._json_indicator.setPixmap(icon.pixmap(16, 16))
            self._json_indicator.setToolTip("No JSON schema")

    def _update_validation(self) -> None:
        """Update validation state and icon."""
        was_valid = self._is_valid

        if self._selector_type == "system":
            # System instruction is optional, always valid
            self._is_valid = True
        else:
            # Prompt is required
            if self._current_value is None:
                self._is_valid = False
            elif self._is_builtin:
                self._is_valid = True
            else:
                # Custom file must exist
                self._is_valid = Path(self._current_value).exists()

        set_validation_icon(self._validation_icon, self._is_valid)

        if was_valid != self._is_valid:
            self.validationChanged.emit(self._is_valid)

    def _on_edit_clicked(self) -> None:
        """Handle edit button click."""
        if self._current_value is None:
            return

        if self._is_builtin:
            # Get path to built-in file
            if self._selector_type == "prompt":
                path, _ = get_prompt(self._current_value)
            else:
                path = get_system_instruction(self._current_value)
            self.editRequested.emit(str(path), True)
        else:
            self.editRequested.emit(self._current_value, False)

    def get_value(self) -> str | None:
        """Get the current selection value.

        Returns
        -------
        str | None
            The selected prompt/instruction name or path, or None if none selected.
        """
        return self._current_value

    def is_builtin(self) -> bool:
        """Check if current selection is a built-in prompt.

        Returns
        -------
        bool
            True if built-in, False if custom file.
        """
        return self._is_builtin

    def is_valid(self) -> bool:
        """Check if current selection is valid.

        Returns
        -------
        bool
            True if valid.
        """
        return self._is_valid

    def has_json_schema(self) -> bool:
        """Check if current prompt has a JSON schema.

        Returns
        -------
        bool
            True if JSON schema exists.
        """
        return self._has_json_schema

    def get_prompt_path(self) -> Path | None:
        """Get the path to the selected prompt file.

        Returns
        -------
        Path | None
            The path to the prompt file.
        """
        if self._current_value is None:
            return None

        if self._is_builtin:
            if self._selector_type == "prompt":
                path, _ = get_prompt(self._current_value)
            else:
                path = get_system_instruction(self._current_value)
            return Path(str(path))
        else:
            return Path(self._current_value)

    def get_json_schema_path(self) -> Path | None:
        """Get the path to the JSON schema file if it exists.

        Returns
        -------
        Path | None
            The path to the JSON schema file, or None.
        """
        if self._selector_type != "prompt" or not self._has_json_schema:
            return None

        if self._is_builtin and self._current_value:
            _, json_path = get_prompt(self._current_value)
            return Path(str(json_path)) if json_path else None
        elif self._custom_path:
            return Path(self._custom_path).with_suffix(".json")

        return None

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the widget.

        Parameters
        ----------
        enabled : bool
            Whether to enable the widget.
        """
        super().setEnabled(enabled)
        self._combo.setEnabled(enabled)
        self._edit_btn.setEnabled(enabled)
