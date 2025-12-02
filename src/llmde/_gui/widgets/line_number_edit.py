"""Text edit widget with line numbers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QColor, QPainter, QTextFormat
from PyQt6.QtWidgets import QPlainTextEdit, QTextEdit, QWidget

from ..utils import GUIConfig

if TYPE_CHECKING:
    from PyQt6.QtGui import QPaintEvent, QResizeEvent


class LineNumberArea(QWidget):
    """Widget for displaying line numbers next to a text editor.

    Parameters
    ----------
    editor : LineNumberTextEdit
        The text editor this line number area belongs to.
    """

    def __init__(self, editor: LineNumberTextEdit) -> None:
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:
        """Get the recommended size for this widget.

        Returns
        -------
        QSize
            The recommended size.
        """
        return QSize(self._editor.line_number_area_width(), 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Handle paint events.

        Parameters
        ----------
        event : QPaintEvent
            The paint event.
        """
        self._editor.line_number_area_paint_event(event)


class LineNumberTextEdit(QPlainTextEdit):
    """Plain text editor with line numbers.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Displays line numbers in a gutter on the left side of the editor.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._line_number_area = LineNumberArea(self)

        # Connect signals for updating line number area
        self.blockCountChanged.connect(self._update_line_number_area_width)
        self.updateRequest.connect(self._update_line_number_area)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_line_number_area_width(0)
        self._highlight_current_line()

        # Set monospace font
        font = self.font()
        font.setFamily("Consolas")
        font.setPointSize(11)
        self.setFont(font)

        # Set tab width
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)

    def line_number_area_width(self) -> int:
        """Calculate the width needed for the line number area.

        Returns
        -------
        int
            The width in pixels.
        """
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1

        # Ensure minimum width for 3 digits plus padding
        digits = max(3, digits)
        space = 10 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    def _update_line_number_area_width(self, _: int) -> None:
        """Update the viewport margins to accommodate line number area.

        Parameters
        ----------
        _ : int
            The new block count (unused).
        """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def _update_line_number_area(self, rect: QRect, dy: int) -> None:
        """Update the line number area when the editor scrolls.

        Parameters
        ----------
        rect : QRect
            The area that needs to be updated.
        dy : int
            The scroll amount in pixels.
        """
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(
                0, rect.y(), self._line_number_area.width(), rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self._update_line_number_area_width(0)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events.

        Parameters
        ----------
        event : QResizeEvent
            The resize event.
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def _highlight_current_line(self) -> None:
        """Highlight the current line."""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(GUIConfig.COLORS["bg_tertiary"])
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event: QPaintEvent) -> None:
        """Paint the line number area.

        Parameters
        ----------
        event : QPaintEvent
            The paint event.
        """
        painter = QPainter(self._line_number_area)

        # Background
        painter.fillRect(event.rect(), QColor(GUIConfig.COLORS["bg_tertiary"]))

        # Draw line numbers
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        bottom = top + round(self.blockBoundingRect(block).height())

        # Line number text color
        painter.setPen(QColor(GUIConfig.COLORS["text_muted"]))

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0,
                    top,
                    self._line_number_area.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

        painter.end()

    def setReadOnly(self, read_only: bool) -> None:
        """Set the read-only state.

        Parameters
        ----------
        read_only : bool
            Whether the editor should be read-only.
        """
        super().setReadOnly(read_only)
        self._highlight_current_line()

        # Update styling for read-only mode
        if read_only:
            self.setStyleSheet(f"background-color: {GUIConfig.COLORS['bg_tertiary']};")
        else:
            self.setStyleSheet("")
