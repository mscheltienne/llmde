"""API key input widget with source indicator and validation."""

from __future__ import annotations

import os
from typing import Literal

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from ..utils import GUIConfig, set_validation_icon


class APIKeyWidget(QWidget):
    """Widget for API key input with source indicator and validation.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Displays an API key input field with:
    - Source indicator icon showing if key is from env var or manual entry
    - Validation icon showing if key is valid (non-empty)
    """

    apiKeyChanged = pyqtSignal(str)
    validationChanged = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._source: Literal["env", "manual", "empty"] = "empty"
        self._current_model: Literal["gemini", "claude"] | None = None
        self._is_valid = False

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        self._label = QLabel("API Key:")
        self._label.setFixedWidth(80)
        layout.addWidget(self._label)

        # API key input (password mode)
        self._input = QLineEdit()
        self._input.setEchoMode(QLineEdit.EchoMode.Password)
        self._input.setPlaceholderText("Enter API key or set environment variable")
        layout.addWidget(self._input, 1)

        # Source indicator icon
        self._source_icon = QLabel()
        self._source_icon.setFixedSize(*GUIConfig.API_KEY_INDICATOR_SIZE)
        self._source_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._source_icon)

        # Validation icon
        self._validation_icon = QLabel()
        self._validation_icon.setFixedSize(*GUIConfig.VALIDATION_ICON_SIZE)
        self._validation_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._validation_icon)

        self._update_source_icon()

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._input.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str) -> None:
        """Handle text changes in the input field.

        Parameters
        ----------
        text : str
            The new text value.
        """
        # If user edits the field, change source to manual
        if self._source == "env":
            self._source = "manual"
            self._update_source_icon()

        self._validate()
        self.apiKeyChanged.emit(text)

    def _validate(self) -> None:
        """Validate the API key and update icons."""
        text = self._input.text().strip()
        was_valid = self._is_valid

        if text:
            self._is_valid = True
            if self._source == "empty":
                self._source = "manual"
                self._update_source_icon()
        else:
            self._is_valid = False
            self._source = "empty"
            self._update_source_icon()

        set_validation_icon(self._validation_icon, self._is_valid)

        if was_valid != self._is_valid:
            self.validationChanged.emit(self._is_valid)

    def _update_source_icon(self) -> None:
        """Update the source indicator icon."""
        icon = GUIConfig.get_api_key_source_icon(self._source)
        size = GUIConfig.API_KEY_INDICATOR_SIZE[0]
        self._source_icon.setPixmap(icon.pixmap(size, size))

        # Set tooltip based on source
        if self._source == "env":
            env_var = self._get_env_var_name()
            self._source_icon.setToolTip(f"Loaded from {env_var}")
        elif self._source == "manual":
            self._source_icon.setToolTip("Manually entered")
        else:
            self._source_icon.setToolTip("API key required")

    def _get_env_var_name(self) -> str:
        """Get the environment variable name for the current model.

        Returns
        -------
        str
            The environment variable name.
        """
        if self._current_model == "gemini":
            return GUIConfig.ENV_VAR_GEMINI_API_KEY
        elif self._current_model == "claude":
            return GUIConfig.ENV_VAR_CLAUDE_API_KEY
        return "LLMDE_*_API_KEY"

    def set_model(self, model: Literal["gemini", "claude"]) -> None:
        """Set the current model and load API key from environment.

        Parameters
        ----------
        model : str
            The model type: 'gemini' or 'claude'.
        """
        self._current_model = model.lower()

        # Try to load from environment variable
        env_var = self._get_env_var_name()
        env_value = os.environ.get(env_var, "")

        if env_value:
            self._source = "env"
            # Block signals to avoid triggering validation twice
            self._input.blockSignals(True)
            self._input.setText(env_value)
            self._input.blockSignals(False)
            self._update_source_icon()
            self._validate()
        else:
            # Clear the field if no env var and keep current manual entry
            # or clear if it was from a different env
            if self._source == "env":
                self._input.clear()
                self._source = "empty"
                self._update_source_icon()
                self._validate()

    def get_api_key(self) -> str:
        """Get the current API key value.

        Returns
        -------
        str
            The API key.
        """
        return self._input.text().strip()

    def is_valid(self) -> bool:
        """Check if the API key is valid.

        Returns
        -------
        bool
            True if the API key is non-empty.
        """
        return self._is_valid

    def get_source(self) -> Literal["env", "manual", "empty"]:
        """Get the API key source.

        Returns
        -------
        str
            The source: 'env', 'manual', or 'empty'.
        """
        return self._source

    def clear(self) -> None:
        """Clear the API key input."""
        self._input.clear()
        self._source = "empty"
        self._update_source_icon()
        self._validate()

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the widget.

        Parameters
        ----------
        enabled : bool
            Whether to enable the widget.
        """
        super().setEnabled(enabled)
        self._input.setEnabled(enabled)
