"""Main window for the LLMDE GUI application."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import qtawesome as qta
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from llmde.io import read_json_schema, read_markdown

from .dialogs import MarkdownEditorDialog
from .utils import GUIConfig, WidgetGroupStateManager, apply_css_class
from .widgets import (
    AnimatedButtonGroup,
    APIKeyWidget,
    PDFDropZone,
    PromptSelectorWidget,
    ResponsePanel,
)

if TYPE_CHECKING:
    from PyQt6.QtGui import QCloseEvent


class ExtractionWorker(QThread):
    """Worker thread for running extractions.

    Parameters
    ----------
    model_type : str
        The model type: 'gemini' or 'claude'.
    model_name : str
        The model name/identifier.
    api_key : str
        The API key.
    prompt_content : str
        The prompt content.
    system_instruction : str | None
        The system instruction content, or None.
    files : list of Path
        List of PDF file paths.
    json_schema : dict | None
        JSON schema for structured output (Gemini only).
    """

    finished = pyqtSignal(str, bool)  # (response, success)
    error = pyqtSignal(str)

    def __init__(
        self,
        model_type: str,
        model_name: str,
        api_key: str,
        prompt_content: str,
        system_instruction: str | None,
        files: list[Path],
        json_schema: dict | None,
    ) -> None:
        super().__init__()
        self._model_type = model_type
        self._model_name = model_name
        self._api_key = api_key
        self._prompt_content = prompt_content
        self._system_instruction = system_instruction
        self._files = files
        self._json_schema = json_schema

    def run(self) -> None:
        """Run the extraction in a background thread."""
        try:
            if self._model_type == "gemini":
                from llmde.models import GeminiModel

                model = GeminiModel(
                    model_name=self._model_name,
                    api_key=self._api_key,
                    system_instruction=self._system_instruction,
                    temperature=0.0,
                )
                response = model.query(
                    self._prompt_content,
                    files=self._files if self._files else None,
                    json_schema=self._json_schema,
                )
            else:  # claude
                from llmde.models import ClaudeModel

                model = ClaudeModel(
                    model_name=self._model_name,
                    api_key=self._api_key,
                    system_instruction=self._system_instruction,
                    temperature=0.0,
                )
                response = model.query(
                    self._prompt_content,
                    files=self._files if self._files else None,
                )

            self.finished.emit(response, True)

        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(str(e), False)


class MainWindow(QMainWindow):
    """Main application window for LLMDE GUI.

    Parameters
    ----------
    parent : QWidget | None
        The parent widget.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._worker: ExtractionWorker | None = None
        self._widget_manager = WidgetGroupStateManager()

        self._setup_ui()
        self._connect_signals()
        self._register_widget_groups()
        self._apply_stylesheet()

        # Set initial model selection
        self._model_selector.set_selected_index(0)

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle(GUIConfig.WINDOW_TITLE)
        self.setMinimumSize(GUIConfig.WINDOW_MIN_WIDTH, GUIConfig.WINDOW_MIN_HEIGHT)
        self.resize(GUIConfig.WINDOW_DEFAULT_WIDTH, GUIConfig.WINDOW_DEFAULT_HEIGHT)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(*GUIConfig.WINDOW_MARGINS)
        main_layout.setSpacing(GUIConfig.SECTION_SPACING)

        # --- Model Selection ---
        model_section = QWidget()
        model_layout = QVBoxLayout(model_section)
        model_layout.setContentsMargins(0, 0, 0, 0)

        self._model_selector = AnimatedButtonGroup(["Gemini", "Claude"])
        model_layout.addWidget(self._model_selector)

        main_layout.addWidget(model_section)

        # --- Model Name Input ---
        model_name_section = QWidget()
        model_name_layout = QHBoxLayout(model_name_section)
        model_name_layout.setContentsMargins(0, 0, 0, 0)

        model_name_label = QLabel("Model:")
        model_name_label.setFixedWidth(80)
        model_name_layout.addWidget(model_name_label)

        self._model_name_input = QLineEdit()
        self._model_name_input.setPlaceholderText("Enter model name")
        model_name_layout.addWidget(self._model_name_input, 1)

        main_layout.addWidget(model_name_section)

        # Separator
        main_layout.addWidget(self._create_separator())

        # --- API Key ---
        self._api_key_widget = APIKeyWidget()
        main_layout.addWidget(self._api_key_widget)

        # Separator
        main_layout.addWidget(self._create_separator())

        # --- System Instruction Selector ---
        self._system_selector = PromptSelectorWidget("system")
        main_layout.addWidget(self._system_selector)

        # --- Prompt Selector ---
        self._prompt_selector = PromptSelectorWidget("prompt")
        main_layout.addWidget(self._prompt_selector)

        # Separator
        main_layout.addWidget(self._create_separator())

        # --- PDF Drop Zone ---
        pdf_section = QWidget()
        pdf_layout = QVBoxLayout(pdf_section)
        pdf_layout.setContentsMargins(0, 0, 0, 0)

        pdf_label = QLabel("PDF Files (optional)")
        pdf_label.setProperty("class", "section-header")
        pdf_layout.addWidget(pdf_label)

        self._pdf_drop_zone = PDFDropZone()
        pdf_layout.addWidget(self._pdf_drop_zone)

        main_layout.addWidget(pdf_section)

        # Separator
        main_layout.addWidget(self._create_separator())

        # --- Run Button ---
        run_section = QWidget()
        run_layout = QHBoxLayout(run_section)
        run_layout.setContentsMargins(0, 0, 0, 0)
        run_layout.addStretch()

        self._run_btn = QPushButton("  Run Extraction")
        self._run_btn.setFixedSize(180, 44)
        run_icon = qta.icon(GUIConfig.ICONS["run"], color="#ffffff")
        self._run_btn.setIcon(run_icon)
        apply_css_class(self._run_btn, "action-button")
        run_layout.addWidget(self._run_btn)

        run_layout.addStretch()
        main_layout.addWidget(run_section)

        # Separator
        main_layout.addWidget(self._create_separator())

        # --- Response Panel ---
        self._response_panel = ResponsePanel()
        main_layout.addWidget(self._response_panel, 1)

    def _create_separator(self) -> QFrame:
        """Create a horizontal separator line.

        Returns
        -------
        QFrame
            The separator widget.
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator

    def _connect_signals(self) -> None:
        """Connect widget signals."""
        # Model selection
        self._model_selector.selectionChanged.connect(self._on_model_changed)

        # Validation changes
        self._api_key_widget.validationChanged.connect(self._update_run_button)
        self._prompt_selector.validationChanged.connect(self._update_run_button)

        # Edit requests
        self._system_selector.editRequested.connect(self._on_edit_prompt)
        self._prompt_selector.editRequested.connect(self._on_edit_prompt)

        # Run button
        self._run_btn.clicked.connect(self._on_run_clicked)

    def _register_widget_groups(self) -> None:
        """Register widget groups for state management."""
        self._widget_manager.register_group(
            "model-selector",
            [*self._model_selector.buttons],
        )
        self._widget_manager.register_group(
            "model-name",
            [self._model_name_input],
        )
        self._widget_manager.register_group(
            "api-key",
            [self._api_key_widget],
        )
        self._widget_manager.register_group(
            "system-instruction",
            [self._system_selector],
        )
        self._widget_manager.register_group(
            "prompt",
            [self._prompt_selector],
        )
        self._widget_manager.register_group(
            "file-drop",
            [self._pdf_drop_zone],
        )
        self._widget_manager.register_group(
            "run-button",
            [self._run_btn],
        )

    def _apply_stylesheet(self) -> None:
        """Apply the application stylesheet."""
        try:
            stylesheet = GUIConfig.load_stylesheet()
            self.setStyleSheet(stylesheet)
        except Exception:
            # Stylesheet loading failed, continue without it
            pass

    def _on_model_changed(self, model: str) -> None:
        """Handle model selection change.

        Parameters
        ----------
        model : str
            The selected model name.
        """
        model_lower = model.lower()
        self._api_key_widget.set_model(model_lower)

        # Set default model name
        if model_lower == "gemini":
            self._model_name_input.setText(GUIConfig.DEFAULT_MODEL_GEMINI)
        else:
            self._model_name_input.setText(GUIConfig.DEFAULT_MODEL_CLAUDE)

        self._update_run_button()

    def _on_edit_prompt(self, path: str, is_builtin: bool) -> None:
        """Handle edit request for prompt or system instruction.

        Parameters
        ----------
        path : str
            The file path.
        is_builtin : bool
            Whether this is a built-in prompt.
        """
        dialog = MarkdownEditorDialog(path, is_builtin, parent=self)
        dialog.exec()

    def _update_run_button(self) -> None:
        """Update run button enabled state based on validation."""
        is_valid = (
            self._api_key_widget.is_valid()
            and self._prompt_selector.is_valid()
            and self._model_name_input.text().strip()
        )
        self._run_btn.setEnabled(is_valid)

    def _on_run_clicked(self) -> None:
        """Handle run button click."""
        if self._worker is not None and self._worker.isRunning():
            return

        # Get model info
        model_label = self._model_selector.selected_label
        if not model_label:
            return

        model_type = model_label.lower()
        model_name = self._model_name_input.text().strip()
        api_key = self._api_key_widget.get_api_key()

        # Get prompt content
        prompt_path = self._prompt_selector.get_prompt_path()
        if not prompt_path:
            return

        prompt_content = read_markdown(prompt_path)

        # Get system instruction content (optional)
        system_instruction = None
        system_path = self._system_selector.get_prompt_path()
        if system_path:
            system_instruction = read_markdown(system_path)

        # Get files
        files = self._pdf_drop_zone.get_files()

        # Get JSON schema for Gemini
        json_schema = None
        if model_type == "gemini" and self._prompt_selector.has_json_schema():
            json_path = self._prompt_selector.get_json_schema_path()
            if json_path:
                json_schema = read_json_schema(json_path)

        # Disable UI during extraction
        self._set_running_state(True)

        # Start worker
        self._worker = ExtractionWorker(
            model_type=model_type,
            model_name=model_name,
            api_key=api_key,
            prompt_content=prompt_content,
            system_instruction=system_instruction,
            files=files,
            json_schema=json_schema,
        )
        self._worker.finished.connect(self._on_extraction_finished)
        self._worker.start()

    def _set_running_state(self, running: bool) -> None:
        """Set the UI state for running/not running.

        Parameters
        ----------
        running : bool
            Whether extraction is running.
        """
        if running:
            # Disable all input widgets
            self._original_states = self._widget_manager.disable_all_groups()

            # Update run button appearance
            self._run_btn.setText("  Running...")
            spinner_icon = qta.icon(
                GUIConfig.ICONS["spinner"],
                color="#ffffff",
                animation=qta.Spin(self._run_btn),
            )
            self._run_btn.setIcon(spinner_icon)

            # Set response panel to loading state
            self._response_panel.set_loading(True)
            self._response_panel.clear()
        else:
            # Restore all input widgets
            if hasattr(self, "_original_states"):
                self._widget_manager.restore_all_groups(self._original_states)

            # Restore run button appearance
            self._run_btn.setText("  Run Extraction")
            run_icon = qta.icon(GUIConfig.ICONS["run"], color="#ffffff")
            self._run_btn.setIcon(run_icon)

            # Clear loading state
            self._response_panel.set_loading(False)

            # Update run button state
            self._update_run_button()

    def _on_extraction_finished(self, response: str, success: bool) -> None:
        """Handle extraction completion.

        Parameters
        ----------
        response : str
            The response text.
        success : bool
            Whether extraction was successful.
        """
        self._set_running_state(False)
        self._response_panel.set_response(response)

        # Clean up worker
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event.

        Parameters
        ----------
        event : QCloseEvent
            The close event.
        """
        # Stop any running worker
        if self._worker is not None and self._worker.isRunning():
            self._worker.terminate()
            self._worker.wait()

        # Clean up widget manager
        self._widget_manager.clear_all()

        event.accept()


def run_gui() -> int:
    """Run the LLMDE GUI application.

    Returns
    -------
    int
        The application exit code.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("LLMDE")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run_gui())
