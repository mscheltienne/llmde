"""Drag-and-drop widget for PDF files."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import QEvent, QObject, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..utils import apply_css_class

if TYPE_CHECKING:
    from PyQt6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent


class PDFDropZone(QWidget):
    """Widget for drag-and-drop PDF file selection.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.

    Notes
    -----
    Accepts only PDF files. Displays dropped files in a list with remove buttons.
    Emits filesChanged signal when files are added or removed.
    """

    filesChanged = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._files: list[str] = []
        self._drag_active = False

        self._setup_ui()
        self.setAcceptDrops(True)

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main horizontal layout: drop zone left, file list right
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        # --- Left side: Drop zone ---
        self._drop_zone = QLabel()
        self._drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._drop_zone.setFixedWidth(220)
        self._drop_zone.setMinimumHeight(140)
        self._drop_zone.setWordWrap(True)
        self._drop_zone.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_drop_zone_text()
        self._apply_drop_zone_style()
        main_layout.addWidget(self._drop_zone)

        # Make drop zone clickable via event filter
        self._drop_zone.installEventFilter(self)

        # --- Right side: File list container ---
        self._file_list_container = QWidget()
        self._file_list_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        file_list_layout = QVBoxLayout(self._file_list_container)
        file_list_layout.setContentsMargins(0, 0, 0, 0)
        file_list_layout.setSpacing(4)

        # Info label
        self._info_label = QLabel("No files selected")
        self._info_label.setProperty("class", "status-text")
        file_list_layout.addWidget(self._info_label)

        # Scroll area for file items
        self._file_scroll_area = QScrollArea()
        self._file_scroll_area.setWidgetResizable(True)
        self._file_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self._file_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._file_scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self._file_scroll_area.setMinimumHeight(110)

        # Container for file items
        self._file_items_widget = QWidget()
        self._file_items_layout = QVBoxLayout(self._file_items_widget)
        self._file_items_layout.setContentsMargins(0, 0, 4, 0)
        self._file_items_layout.setSpacing(2)
        self._file_items_layout.addStretch()

        self._file_scroll_area.setWidget(self._file_items_widget)
        file_list_layout.addWidget(self._file_scroll_area, 1)

        main_layout.addWidget(self._file_list_container, 1)

    def _update_drop_zone_text(self) -> None:
        """Update the drop zone text based on current state."""
        if self._drag_active:
            self._drop_zone.setText("Drop PDF files here")
        else:
            self._drop_zone.setText(
                "Drag and drop PDF files here\n\nor click to browse"
            )

    def _apply_drop_zone_style(self) -> None:
        """Apply styling to the drop zone based on current state."""
        if self._drag_active:
            apply_css_class(self._drop_zone, "drop-zone-active")
        else:
            apply_css_class(self._drop_zone, "drop-zone")

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filter events for the drop zone widget.

        Parameters
        ----------
        obj : QObject
            The object that received the event.
        event : QEvent
            The event.

        Returns
        -------
        bool
            True if the event was handled, False otherwise.
        """
        if obj is self._drop_zone and event.type() == QEvent.Type.MouseButtonPress:
            self._browse_files()
            return True
        return super().eventFilter(obj, event)

    def _browse_files(self) -> None:
        """Open file dialog to browse for PDF files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF Files",
            "",
            "PDF Files (*.pdf);;All Files (*)",
        )

        if files:
            new_files = [f for f in files if f not in self._files]
            if new_files:
                self._files.extend(new_files)
                self._update_file_list()
                self.filesChanged.emit()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Handle drag enter events.

        Parameters
        ----------
        event : QDragEnterEvent
            The drag enter event.
        """
        if event.mimeData().hasUrls():
            # Check if any files are PDFs
            valid_files = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if file_path.lower().endswith(".pdf"):
                        valid_files.append(file_path)

            if valid_files:
                event.acceptProposedAction()
                self._drag_active = True
                self._update_drop_zone_text()
                self._apply_drop_zone_style()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        """Handle drag leave events.

        Parameters
        ----------
        event : QDragLeaveEvent
            The drag leave event.
        """
        self._drag_active = False
        self._update_drop_zone_text()
        self._apply_drop_zone_style()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle drop events.

        Parameters
        ----------
        event : QDropEvent
            The drop event.
        """
        if event.mimeData().hasUrls():
            new_files = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if file_path.lower().endswith(".pdf"):
                        if file_path not in self._files:
                            new_files.append(file_path)

            if new_files:
                self._files.extend(new_files)
                self._update_file_list()
                self.filesChanged.emit()
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

        self._drag_active = False
        self._update_drop_zone_text()
        self._apply_drop_zone_style()

    def _update_file_list(self) -> None:
        """Update the file list display."""
        self._clear_file_items()

        if not self._files:
            self._info_label.setText("No files selected")
            return

        for file_path in self._files:
            self._create_file_item_widget(file_path)

        file_count = len(self._files)
        self._info_label.setText(
            f"{file_count} PDF file{'s' if file_count != 1 else ''} selected"
        )

    def _clear_file_items(self) -> None:
        """Clear all file item widgets from the layout."""
        while self._file_items_layout.count() > 1:
            child = self._file_items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _create_file_item_widget(self, file_path: str) -> None:
        """Create a file item widget with remove button.

        Parameters
        ----------
        file_path : str
            The full path to the file.
        """
        file_widget = QWidget()
        apply_css_class(file_widget, "file-item")
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(6, 4, 6, 4)
        file_layout.setSpacing(6)

        # Filename label with elided text
        filename = Path(file_path).name
        file_label = QLabel(filename)
        file_label.setToolTip(file_path)

        # Use text elision for long filenames
        file_label.setMinimumWidth(50)
        file_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        # Truncate display if needed (longer limit now)
        if len(filename) > 55:
            display_name = filename[:52] + "..."
            file_label.setText(display_name)

        file_layout.addWidget(file_label, 1)

        # Remove button
        remove_btn = QPushButton("✕")
        remove_btn.setFixedSize(18, 18)
        remove_btn.setToolTip(f"Remove {filename}")
        apply_css_class(remove_btn, "file-remove-button")
        remove_btn.clicked.connect(lambda: self._remove_file(file_path))
        file_layout.addWidget(remove_btn)

        # Insert before the stretch
        insert_index = self._file_items_layout.count() - 1
        self._file_items_layout.insertWidget(insert_index, file_widget)

    def _remove_file(self, file_path: str) -> None:
        """Remove a file from the list.

        Parameters
        ----------
        file_path : str
            The path of the file to remove.
        """
        if file_path in self._files:
            self._files.remove(file_path)
            self._update_file_list()
            self.filesChanged.emit()

    def get_files(self) -> list[Path]:
        """Get the list of selected files.

        Returns
        -------
        list of Path
            List of file paths.
        """
        return [Path(f) for f in self._files]

    def get_file_paths(self) -> list[str]:
        """Get the list of selected file paths as strings.

        Returns
        -------
        list of str
            List of file path strings.
        """
        return list(self._files)

    def clear_files(self) -> None:
        """Clear all files from the widget."""
        if self._files:
            self._files.clear()
            self._update_file_list()
            self.filesChanged.emit()

    def has_files(self) -> bool:
        """Check if any files are selected.

        Returns
        -------
        bool
            True if files are present.
        """
        return len(self._files) > 0

    def file_count(self) -> int:
        """Get the number of selected files.

        Returns
        -------
        int
            The number of files.
        """
        return len(self._files)

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the widget.

        Parameters
        ----------
        enabled : bool
            Whether to enable the widget.
        """
        super().setEnabled(enabled)
        self.setAcceptDrops(enabled)
        if enabled:
            self._drop_zone.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self._drop_zone.setCursor(Qt.CursorShape.ForbiddenCursor)
