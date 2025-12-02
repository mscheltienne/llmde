"""Validation framework for GUI input fields."""

from __future__ import annotations

from typing import TYPE_CHECKING

import qtawesome as qta

from .config import GUIConfig

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QLabel, QWidget


class ValidationField:
    """Configuration for a validation field.

    Parameters
    ----------
    name : str
        Unique identifier for this field.
    icon_widget : QLabel
        The QLabel widget that displays the validation icon.
    required : bool
        Whether this field is required for form submission.
    """

    def __init__(
        self, name: str, icon_widget: QLabel, required: bool = True
    ) -> None:
        self.name = name
        self.icon_widget = icon_widget
        self.required = required
        self._valid = False

    @property
    def valid(self) -> bool:
        """Get the validation state.

        Returns
        -------
        bool
            True if the field is valid, False otherwise.
        """
        return self._valid

    @valid.setter
    def valid(self, value: bool) -> None:
        """Set the validation state.

        Parameters
        ----------
        value : bool
            The new validation state.
        """
        self._valid = value


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


def clear_validation_icon(icon_widget: QLabel) -> None:
    """Clear the validation icon from a QLabel widget.

    Parameters
    ----------
    icon_widget : QLabel
        The QLabel to clear.
    """
    icon_widget.clear()


def set_warning_icon(icon_widget: QLabel, tooltip: str = "") -> None:
    """Set a warning icon on a QLabel widget.

    Parameters
    ----------
    icon_widget : QLabel
        The QLabel to set the icon on.
    tooltip : str
        Optional tooltip text.
    """
    icon = qta.icon(
        GUIConfig.ICONS["warning"], color=GUIConfig.COLORS["validation_warning"]
    )
    size = GUIConfig.VALIDATION_ICON_SIZE[0]
    icon_widget.setPixmap(icon.pixmap(size, size))
    if tooltip:
        icon_widget.setToolTip(tooltip)


def set_info_icon(icon_widget: QLabel, tooltip: str = "") -> None:
    """Set an info icon on a QLabel widget.

    Parameters
    ----------
    icon_widget : QLabel
        The QLabel to set the icon on.
    tooltip : str
        Optional tooltip text.
    """
    icon = qta.icon(GUIConfig.ICONS["info"], color=GUIConfig.COLORS["accent_primary"])
    size = GUIConfig.VALIDATION_ICON_SIZE[0]
    icon_widget.setPixmap(icon.pixmap(size, size))
    if tooltip:
        icon_widget.setToolTip(tooltip)
