"""Animated button group widget for model selection."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from ..utils import GUIConfig, apply_css_class

if TYPE_CHECKING:
    from PyQt6.QtGui import QResizeEvent


class AnimatedButtonGroup(QWidget):
    """Animated button group with sliding highlight.

    Parameters
    ----------
    button_labels : list of str
        List of labels for the buttons to create.
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Emits a ``selectionChanged`` signal when a button is clicked.
    """

    selectionChanged = pyqtSignal(str)

    def __init__(
        self, button_labels: list[str], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        if len(button_labels) == 0:
            raise ValueError("button_labels must not be empty")
        self._button_labels = button_labels
        self._buttons: list[QPushButton] = []
        self._selected_index: int | None = None
        self._highlight_widget = QWidget(self)
        self._animation = QPropertyAnimation(self._highlight_widget, b"geometry")

        self._setup_ui()
        self._setup_highlight()
        self._setup_animation()

    @property
    def buttons(self) -> tuple[QPushButton, ...]:
        """Get read-only access to the buttons list.

        Returns
        -------
        tuple of QPushButton
            The tuple of buttons in this group.
        """
        return tuple(self._buttons)

    @property
    def selected_label(self) -> str | None:
        """Get the currently selected button label.

        Returns
        -------
        str | None
            The label of the selected button, or None if no selection.
        """
        if self._selected_index is None:
            return None
        return self._button_labels[self._selected_index]

    @property
    def selected_index(self) -> int | None:
        """Get the currently selected button index.

        Returns
        -------
        int | None
            The index of the selected button, or None if no selection.
        """
        return self._selected_index

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(*GUIConfig.BUTTON_GROUP_MARGINS)
        layout.setSpacing(GUIConfig.BUTTON_GROUP_SPACING)
        layout.addStretch()

        for i, label in enumerate(self._button_labels):
            button = QPushButton(label)
            button.setCheckable(False)
            # Calculate button width based on text content with padding
            button_width = max(
                GUIConfig.MODEL_BUTTON_SIZE[0], len(label) * 10 + 40
            )
            button.setFixedSize(button_width, GUIConfig.MODEL_BUTTON_SIZE[1])
            button.setProperty("class", "model-button")
            button.clicked.connect(lambda _, idx=i: self._on_button_clicked(idx))
            self._buttons.append(button)
            layout.addWidget(button)

        layout.addStretch()
        self._apply_styles()

    def _setup_highlight(self) -> None:
        """Set up the highlight widget."""
        self._highlight_widget.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self._highlight_widget.lower()
        self._update_highlight_position()

    def _setup_animation(self) -> None:
        """Set up the animation properties."""
        self._animation.setDuration(GUIConfig.ANIMATION_DURATION)
        self._animation.setEasingCurve(GUIConfig.ANIMATION_EASING)

    def _update_highlight_position(self) -> None:
        """Update highlight position to match selected button."""
        if self._buttons and self._selected_index is not None:
            button = self._buttons[self._selected_index]
            self._highlight_widget.setGeometry(button.geometry())
            self._highlight_widget.show()
        elif self._selected_index is None:
            self._highlight_widget.hide()

    def _on_button_clicked(self, index: int) -> None:
        """Handle button click and animate to new selection.

        Parameters
        ----------
        index : int
            Index of the clicked button.
        """
        if index == self._selected_index:
            return

        old_index = self._selected_index
        self._selected_index = index
        self._apply_styles()

        # Animate highlight if we had a previous selection
        if old_index is not None:
            start_rect = self._buttons[old_index].geometry()
            end_rect = self._buttons[index].geometry()
            self._animation.setStartValue(start_rect)
            self._animation.setEndValue(end_rect)
            self._animation.start()
        else:
            self._update_highlight_position()
            self._highlight_widget.show()

        self.selectionChanged.emit(self._button_labels[index])

    def _apply_styles(self) -> None:
        """Apply current styles to all components."""
        for k, button in enumerate(self._buttons):
            is_selected = (
                self._selected_index is not None and k == self._selected_index
            )
            button.setProperty(
                "class",
                "model-button-selected" if is_selected else "model-button",
            )
            button.style().unpolish(button)
            button.style().polish(button)

        apply_css_class(self._highlight_widget, "highlight")

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events and update highlight position.

        Parameters
        ----------
        event : QResizeEvent
            The resize event.
        """
        super().resizeEvent(event)
        self._update_highlight_position()

    def set_selected_index(self, index: int | None) -> None:
        """Set the selected index programmatically without animation.

        Parameters
        ----------
        index : int | None
            Index of the button to select, or None to clear selection.
        """
        if index is not None and not (0 <= index < len(self._buttons)):
            raise ValueError(f"Index {index} out of range")
        if index == self._selected_index:
            return

        self._selected_index = index
        self._apply_styles()
        self._update_highlight_position()

        if index is not None:
            self.selectionChanged.emit(self._button_labels[index])

    def set_selected_label(self, label: str) -> None:
        """Set the selected button by label.

        Parameters
        ----------
        label : str
            The label of the button to select.
        """
        try:
            index = self._button_labels.index(label)
            self.set_selected_index(index)
        except ValueError:
            raise ValueError(f"Label '{label}' not found in button labels")

    def clear_selection(self) -> None:
        """Clear the current selection (no button selected)."""
        self.set_selected_index(None)
