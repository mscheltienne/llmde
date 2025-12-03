"""Widget for generation parameters (temperature, top_p, top_k, max_tokens)."""

from __future__ import annotations

import qtawesome as qta
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from superqt import QLabeledDoubleSlider

from ..utils import GUIConfig


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
        self._apply_slider_styles()

    def _create_info_icon(self, tooltip: str) -> QLabel:
        """Create an info icon label with tooltip.

        Parameters
        ----------
        tooltip : str
            The tooltip text to display on hover.

        Returns
        -------
        QLabel
            The info icon label.
        """
        icon_label = QLabel()
        icon = qta.icon(GUIConfig.ICONS["info"], color=GUIConfig.COLORS["text_muted"])
        icon_label.setPixmap(icon.pixmap(14, 14))
        icon_label.setToolTip(tooltip)
        icon_label.setToolTipDuration(5000)  # Show for 5 seconds
        icon_label.setCursor(Qt.CursorShape.PointingHandCursor)
        return icon_label

    def _apply_slider_styles(self) -> None:
        """Apply stylesheet to the internal QSlider widgets."""
        # Generate stylesheet using GUIConfig colors
        slider_style = f"""
            QSlider::groove:horizontal {{
                border: 1px solid {GUIConfig.COLORS["border_primary"]};
                background: {GUIConfig.COLORS["button_bg"]};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {GUIConfig.COLORS["accent_primary"]};
                border: 1px solid {GUIConfig.COLORS["accent_primary_hover"]};
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {GUIConfig.COLORS["accent_primary_hover"]};
            }}
            QSlider::handle:horizontal:pressed {{
                background: {GUIConfig.COLORS["accent_primary_pressed"]};
            }}
            QSlider::sub-page:horizontal {{
                background: {GUIConfig.COLORS["accent_primary"]};
                border: 1px solid {GUIConfig.COLORS["accent_primary_hover"]};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::add-page:horizontal {{
                background: {GUIConfig.COLORS["button_bg"]};
                border: 1px solid {GUIConfig.COLORS["border_primary"]};
                height: 8px;
                border-radius: 4px;
            }}
        """
        # Find and style all QSlider children within the QLabeledDoubleSliders
        for slider in self.findChildren(QSlider):
            slider.setStyleSheet(slider_style)

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # --- Row 0: Temperature and Top P ---
        row0 = QHBoxLayout()
        row0.setSpacing(20)

        # Temperature (0.0 - 1.0)
        temp_container = QVBoxLayout()
        temp_container.setSpacing(4)

        temp_header = QHBoxLayout()
        temp_header.setSpacing(4)
        temp_label = QLabel("Temperature")
        temp_header.addWidget(temp_label)
        temp_info = self._create_info_icon(
            "Controls randomness in output.\n"
            "0.0 = deterministic (recommended)\n"
            "1.0 = maximum creativity"
        )
        temp_header.addWidget(temp_info)
        temp_header.addStretch()
        temp_container.addLayout(temp_header)

        self._temperature = QLabeledDoubleSlider(Qt.Orientation.Horizontal)
        self._temperature.setRange(0.0, 1.0)
        self._temperature.setValue(0.0)
        self._temperature.setDecimals(2)
        self._temperature.setSingleStep(0.05)
        temp_container.addWidget(self._temperature)

        row0.addLayout(temp_container, 1)

        # Top P (0.0 - 1.0)
        top_p_container = QVBoxLayout()
        top_p_container.setSpacing(4)

        top_p_header = QHBoxLayout()
        top_p_header.setSpacing(4)
        top_p_label = QLabel("Top P")
        top_p_header.addWidget(top_p_label)
        top_p_info = self._create_info_icon(
            "Nucleus sampling threshold.\n"
            "Lower = more focused output\n"
            "1.0 = consider all tokens"
        )
        top_p_header.addWidget(top_p_info)
        top_p_header.addStretch()
        top_p_container.addLayout(top_p_header)

        self._top_p = QLabeledDoubleSlider(Qt.Orientation.Horizontal)
        self._top_p.setRange(0.0, 1.0)
        self._top_p.setValue(1.0)
        self._top_p.setDecimals(2)
        self._top_p.setSingleStep(0.05)
        top_p_container.addWidget(self._top_p)

        row0.addLayout(top_p_container, 1)

        layout.addLayout(row0)

        # --- Row 1: Top K and Max Tokens ---
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        # Top K (1 - 100)
        top_k_container = QHBoxLayout()
        top_k_container.setSpacing(6)
        top_k_label = QLabel("Top K")
        top_k_container.addWidget(top_k_label)
        top_k_info = self._create_info_icon(
            "Limits token candidates.\n"
            "1 = greedy (most deterministic)\n"
            "40 = balanced (default)"
        )
        top_k_container.addWidget(top_k_info)

        self._top_k = QSpinBox()
        self._top_k.setRange(1, 100)
        self._top_k.setValue(40)
        self._top_k.setFixedWidth(80)
        top_k_container.addWidget(self._top_k)
        top_k_container.addStretch()

        row1.addLayout(top_k_container, 1)

        # Max Tokens
        max_tokens_container = QHBoxLayout()
        max_tokens_container.setSpacing(6)
        max_tokens_label = QLabel("Max Tokens")
        max_tokens_container.addWidget(max_tokens_label)

        self._max_tokens = QSpinBox()
        self._max_tokens.setRange(256, 32768)
        self._max_tokens.setValue(8192)
        self._max_tokens.setSingleStep(256)
        self._max_tokens.setFixedWidth(100)
        max_tokens_container.addWidget(self._max_tokens)
        max_tokens_container.addStretch()

        row1.addLayout(max_tokens_container, 1)

        layout.addLayout(row1)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._temperature.valueChanged.connect(self._on_parameter_changed)
        self._top_p.valueChanged.connect(self._on_parameter_changed)
        self._top_k.valueChanged.connect(self._on_parameter_changed)
        self._max_tokens.valueChanged.connect(self._on_parameter_changed)

    def _on_parameter_changed(self) -> None:
        """Handle parameter value changes."""
        self.parametersChanged.emit()

    def get_temperature(self) -> float:
        """Get the temperature value.

        Returns
        -------
        float
            The temperature value (0.0-1.0).
        """
        return self._temperature.value()

    def get_top_p(self) -> float | None:
        """Get the top_p value.

        Returns
        -------
        float | None
            The top_p value, or None if at default (1.0).
        """
        value = self._top_p.value()
        return value if value < 1.0 else None

    def get_top_k(self) -> int | None:
        """Get the top_k value.

        Returns
        -------
        int | None
            The top_k value, or None if at default (40).
        """
        value = self._top_k.value()
        return value if value != 40 else None

    def get_max_tokens(self) -> int:
        """Get the max_tokens value.

        Returns
        -------
        int
            The max_tokens value.
        """
        return self._max_tokens.value()

    def get_parameters(self) -> dict:
        """Get all generation parameters as a dictionary.

        Returns
        -------
        dict
            Dictionary with temperature, top_p, top_k, max_tokens.
        """
        return {
            "temperature": self.get_temperature(),
            "top_p": self.get_top_p(),
            "top_k": self.get_top_k(),
            "max_tokens": self.get_max_tokens(),
        }

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable all controls.

        Parameters
        ----------
        enabled : bool
            Whether to enable the controls.
        """
        super().setEnabled(enabled)
        self._temperature.setEnabled(enabled)
        self._top_p.setEnabled(enabled)
        self._top_k.setEnabled(enabled)
        self._max_tokens.setEnabled(enabled)
