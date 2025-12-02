"""GUI configuration constants and utilities."""

from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING

import qtawesome as qta
from PyQt6.QtCore import QEasingCurve

if TYPE_CHECKING:
    from PyQt6.QtGui import QIcon


class GUIConfig:
    """Central configuration class for GUI constants and utilities.

    This class provides all configuration values for the LLMDE GUI including
    colors, sizes, margins, animation parameters, and icon definitions.
    """

    # --- Window Settings ---
    WINDOW_TITLE = "LLMDE - Data Extraction"
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 800
    WINDOW_DEFAULT_WIDTH = 800
    WINDOW_DEFAULT_HEIGHT = 900

    # --- Colors ---
    COLORS = {
        # Background colors
        "bg_primary": "#f5f5f5",
        "bg_secondary": "#ffffff",
        "bg_tertiary": "#e8e8e8",
        # Text colors
        "text_primary": "#333333",
        "text_secondary": "#666666",
        "text_muted": "#999999",
        # Border colors
        "border_primary": "#d0d0d0",
        "border_secondary": "#e0e0e0",
        "border_focus": "#4a90e2",
        # Button colors
        "button_bg": "#e0e0e0",
        "button_hover": "#d0d0d0",
        "button_pressed": "#c0c0c0",
        # Accent colors
        "accent_primary": "#4a90e2",
        "accent_secondary": "#28a745",
        "accent_gemini": "#4285f4",  # Google blue
        "accent_claude": "#d97706",  # Anthropic orange/amber
        # Validation colors
        "validation_success": "#4CAF50",
        "validation_error": "#f44336",
        "validation_warning": "#ff9800",
        # Disabled state colors
        "bg_disabled": "#f0f0f0",
        "text_disabled": "#999999",
        "border_disabled": "#e0e0e0",
        "button_disabled": "#e8e8e8",
        "opacity_disabled": "0.5",
        # Drop zone colors
        "drop_zone_bg": "#fafafa",
        "drop_zone_border": "#c0c0c0",
        "drop_zone_active_bg": "#e3f2fd",
        "drop_zone_active_border": "#4a90e2",
        # Highlight colors
        "highlight_bg": "#4a90e2",
        "highlight_text": "#ffffff",
        # Response panel
        "response_bg": "#1e1e1e",
        "response_text": "#d4d4d4",
    }

    # --- Layout Margins and Spacing ---
    WINDOW_MARGINS = (20, 20, 20, 20)  # left, top, right, bottom
    SECTION_MARGINS = (0, 10, 0, 10)
    WIDGET_MARGINS = (0, 5, 0, 5)
    BUTTON_GROUP_MARGINS = (0, 0, 0, 0)
    BUTTON_GROUP_SPACING = 10
    LAYOUT_SPACING = 10
    SECTION_SPACING = 15

    # --- Widget Sizes ---
    BUTTON_HEIGHT = 36
    BUTTON_MIN_WIDTH = 100
    MODEL_BUTTON_SIZE = (120, 40)
    ICON_BUTTON_SIZE = (32, 32)
    VALIDATION_ICON_SIZE = (20, 20)
    API_KEY_INDICATOR_SIZE = (24, 24)

    # --- Animation Settings ---
    ANIMATION_DURATION = 200  # milliseconds
    ANIMATION_EASING = QEasingCurve.Type.OutCubic

    # --- Font Settings ---
    FONT_FAMILY_MONOSPACE = "Consolas, 'Courier New', monospace"
    FONT_SIZE_NORMAL = 13
    FONT_SIZE_SMALL = 11
    FONT_SIZE_LARGE = 15

    # --- Icon Definitions (QtAwesome) ---
    ICONS = {
        # Model icons
        "gemini": "mdi6.google",
        "claude": "mdi6.robot-outline",
        # Validation icons
        "valid": "fa5s.check-circle",
        "invalid": "fa5s.times-circle",
        "warning": "fa5s.exclamation-circle",
        # API key source icons
        "key_env": "fa5s.key",
        "key_manual": "fa5s.edit",
        "key_empty": "fa5s.exclamation-triangle",
        # Action icons
        "run": "fa5s.play",
        "edit": "fa5s.edit",
        "copy": "fa5s.copy",
        "browse": "fa5s.folder-open",
        "clear": "fa5s.times",
        "refresh": "fa5s.sync-alt",
        # File icons
        "pdf": "fa5s.file-pdf",
        "json": "fa5s.file-code",
        "markdown": "fa5s.file-alt",
        # Status icons
        "spinner": "fa5s.spinner",
        "info": "fa5s.info-circle",
    }

    # --- Environment Variable Names ---
    ENV_VAR_GEMINI_API_KEY = "LLMDE_GEMINI_API_KEY"
    ENV_VAR_CLAUDE_API_KEY = "LLMDE_CLAUDE_API_KEY"

    # --- Default Model Names ---
    DEFAULT_MODEL_GEMINI = "gemini-2.0-flash"
    DEFAULT_MODEL_CLAUDE = "claude-sonnet-4-5-20250929"

    @classmethod
    def get_stylesheet_path(cls) -> str:
        """Get the path to the application stylesheet.

        Returns
        -------
        str
            Path to the style.css file.
        """
        return str(files("llmde._gui.assets") / "style.css")

    @classmethod
    def load_stylesheet(cls) -> str:
        """Load and return the application stylesheet content.

        Returns
        -------
        str
            The CSS stylesheet content.
        """
        style_file = files("llmde._gui.assets") / "style.css"
        return style_file.read_text(encoding="utf-8")

    @classmethod
    def get_icon(
        cls, icon_name: str, color: str | None = None, size: int = 16
    ) -> QIcon:
        """Get a QtAwesome icon by name.

        Parameters
        ----------
        icon_name : str
            The icon name from ICONS dictionary or a direct QtAwesome icon name.
        color : str | None
            The icon color. If None, uses text_primary color.
        size : int
            The icon size in pixels.

        Returns
        -------
        QIcon
            The requested icon.
        """
        # Resolve icon name from dictionary if needed
        qta_name = cls.ICONS.get(icon_name, icon_name)
        if color is None:
            color = cls.COLORS["text_secondary"]
        return qta.icon(qta_name, color=color)

    @classmethod
    def get_validation_icon(cls, is_valid: bool) -> QIcon:
        """Get validation icon (checkmark or X).

        Parameters
        ----------
        is_valid : bool
            Whether to get the valid (checkmark) or invalid (X) icon.

        Returns
        -------
        QIcon
            The validation icon.
        """
        if is_valid:
            return qta.icon(cls.ICONS["valid"], color=cls.COLORS["validation_success"])
        return qta.icon(cls.ICONS["invalid"], color=cls.COLORS["validation_error"])

    @classmethod
    def get_api_key_source_icon(cls, source: str) -> QIcon:
        """Get icon for API key source indicator.

        Parameters
        ----------
        source : str
            The source type: 'env', 'manual', or 'empty'.

        Returns
        -------
        QIcon
            The source indicator icon.
        """
        if source == "env":
            return qta.icon(cls.ICONS["key_env"], color=cls.COLORS["accent_primary"])
        elif source == "manual":
            return qta.icon(cls.ICONS["key_manual"], color=cls.COLORS["text_secondary"])
        else:  # empty
            return qta.icon(
                cls.ICONS["key_empty"], color=cls.COLORS["validation_warning"]
            )
