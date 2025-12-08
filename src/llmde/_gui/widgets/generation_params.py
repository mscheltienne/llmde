"""Widget for generation parameters (temperature, top_p, top_k, max_tokens)."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QLabel,
    QSpinBox,
    QWidget,
)
from superqt import QToggleSwitch


class GenerationParametersWidget(QWidget):
    """Widget for configuring LLM generation parameters.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Provides controls for temperature, top_p, top_k, and max_tokens.
    Default values are set for deterministic extraction tasks.
    """

    parametersChanged = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setColumnStretch(3, 1)  # Stretch the last column

        # --- Row 0: Temperature (0.0 - 1.0) with API default toggle ---
        self._temperature_label = QLabel("Temperature")
        layout.addWidget(self._temperature_label, 0, 0)
        self._temperature = QDoubleSpinBox()
        self._temperature.setRange(0.0, 1.0)
        self._temperature.setValue(0.0)
        self._temperature.setDecimals(2)
        self._temperature.setSingleStep(0.05)
        layout.addWidget(self._temperature, 0, 1)
        self._temperature_default_toggle = QToggleSwitch()
        self._temperature_default_toggle.setChecked(False)
        layout.addWidget(self._temperature_default_toggle, 0, 2)
        layout.addWidget(QLabel("API default"), 0, 3)

        # --- Row 1: Top P (0.0 - 1.0) with API default toggle ---
        self._top_p_label = QLabel("Top P")
        layout.addWidget(self._top_p_label, 1, 0)
        self._top_p = QDoubleSpinBox()
        self._top_p.setRange(0.0, 1.0)
        self._top_p.setValue(0.95)
        self._top_p.setDecimals(2)
        self._top_p.setSingleStep(0.05)
        layout.addWidget(self._top_p, 1, 1)
        self._top_p_default_toggle = QToggleSwitch()
        self._top_p_default_toggle.setChecked(True)
        layout.addWidget(self._top_p_default_toggle, 1, 2)
        layout.addWidget(QLabel("API default"), 1, 3)

        # --- Row 2: Top K (1 - 100) with API default toggle ---
        self._top_k_label = QLabel("Top K")
        layout.addWidget(self._top_k_label, 2, 0)
        self._top_k = QSpinBox()
        self._top_k.setRange(1, 100)
        self._top_k.setValue(40)
        layout.addWidget(self._top_k, 2, 1)
        self._top_k_default_toggle = QToggleSwitch()
        self._top_k_default_toggle.setChecked(True)
        layout.addWidget(self._top_k_default_toggle, 2, 2)
        layout.addWidget(QLabel("API default"), 2, 3)

        # --- Row 3: Max Tokens (no API default toggle) ---
        self._max_tokens_label = QLabel("Max Tokens")
        layout.addWidget(self._max_tokens_label, 3, 0)
        self._max_tokens = QSpinBox()
        self._max_tokens.setRange(256, 32768)
        self._max_tokens.setValue(4096)
        self._max_tokens.setSingleStep(256)
        layout.addWidget(self._max_tokens, 3, 1)

        # Apply initial toggle states
        self._on_temperature_toggle_changed(False)
        self._on_top_p_toggle_changed(True)
        self._on_top_k_toggle_changed(True)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._temperature.valueChanged.connect(self._on_parameter_changed)
        self._top_p.valueChanged.connect(self._on_parameter_changed)
        self._top_k.valueChanged.connect(self._on_parameter_changed)
        self._max_tokens.valueChanged.connect(self._on_parameter_changed)
        self._temperature_default_toggle.toggled.connect(
            self._on_temperature_toggle_changed
        )
        self._top_p_default_toggle.toggled.connect(self._on_top_p_toggle_changed)
        self._top_k_default_toggle.toggled.connect(self._on_top_k_toggle_changed)

    def _on_temperature_toggle_changed(self, use_default: bool) -> None:
        """Handle temperature API default toggle change."""
        self._temperature_label.setEnabled(not use_default)
        self._temperature.setEnabled(not use_default)
        self._on_parameter_changed()

    def _on_top_p_toggle_changed(self, use_default: bool) -> None:
        """Handle top_p API default toggle change."""
        self._top_p_label.setEnabled(not use_default)
        self._top_p.setEnabled(not use_default)
        self._on_parameter_changed()

    def _on_top_k_toggle_changed(self, use_default: bool) -> None:
        """Handle top_k API default toggle change."""
        self._top_k_label.setEnabled(not use_default)
        self._top_k.setEnabled(not use_default)
        self._on_parameter_changed()

    def _on_parameter_changed(self) -> None:
        """Handle parameter value changes."""
        self.parametersChanged.emit()

    def get_temperature(self) -> float | None:
        """Get the temperature value, or None if using API default."""
        if self._temperature_default_toggle.isChecked():
            return None
        return self._temperature.value()

    def get_top_p(self) -> float | None:
        """Get the top_p value, or None if using API default."""
        if self._top_p_default_toggle.isChecked():
            return None
        return self._top_p.value()

    def get_top_k(self) -> int | None:
        """Get the top_k value, or None if using API default."""
        if self._top_k_default_toggle.isChecked():
            return None
        return self._top_k.value()

    def get_max_tokens(self) -> int:
        """Get the max_tokens value."""
        return self._max_tokens.value()

    def get_parameters(self) -> dict:
        """Get all generation parameters as a dictionary."""
        return {
            "temperature": self.get_temperature(),
            "top_p": self.get_top_p(),
            "top_k": self.get_top_k(),
            "max_tokens": self.get_max_tokens(),
        }

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable all controls."""
        super().setEnabled(enabled)
        # Temperature (respects API default toggle)
        temp_enabled = enabled and not self._temperature_default_toggle.isChecked()
        self._temperature_label.setEnabled(temp_enabled)
        self._temperature.setEnabled(temp_enabled)
        self._temperature_default_toggle.setEnabled(enabled)
        # Top P (respects API default toggle)
        top_p_enabled = enabled and not self._top_p_default_toggle.isChecked()
        self._top_p_label.setEnabled(top_p_enabled)
        self._top_p.setEnabled(top_p_enabled)
        self._top_p_default_toggle.setEnabled(enabled)
        # Top K (respects API default toggle)
        top_k_enabled = enabled and not self._top_k_default_toggle.isChecked()
        self._top_k_label.setEnabled(top_k_enabled)
        self._top_k.setEnabled(top_k_enabled)
        self._top_k_default_toggle.setEnabled(enabled)
        # Max Tokens (no API default toggle)
        self._max_tokens_label.setEnabled(enabled)
        self._max_tokens.setEnabled(enabled)
