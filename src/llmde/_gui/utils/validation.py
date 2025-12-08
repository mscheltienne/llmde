"""Validation framework for GUI input fields."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .config import GUIConfig

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QLabel, QWidget


def apply_css_class(widget: QWidget, css_class: str) -> None:
    """Apply a CSS class to a widget and refresh its styling.

    Parameters
    ----------
    widget : QWidget
        The widget to apply the class to.
    css_class : str
        The CSS class name to apply.
    """
    widget.setProperty("class", css_class)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def remove_css_class(widget: QWidget) -> None:
    """Remove CSS class from a widget and refresh its styling.

    Parameters
    ----------
    widget : QWidget
        The widget to remove the class from.
    """
    widget.setProperty("class", "")
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def set_validation_icon(icon_widget: QLabel, is_valid: bool) -> None:
    """Set the validation icon on a QLabel widget.

    Parameters
    ----------
    icon_widget : QLabel
        The QLabel to set the icon on.
    is_valid : bool
        Whether to show the valid (checkmark) or invalid (X) icon.
    """
    icon = GUIConfig.get_validation_icon(is_valid)
    size = GUIConfig.VALIDATION_ICON_SIZE[0]
    icon_widget.setPixmap(icon.pixmap(size, size))
