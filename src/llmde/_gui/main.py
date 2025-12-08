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
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..io import read_markdown
from ..models import ClaudeModel, GeminiModel
from .dialogs import MarkdownEditorDialog
from .utils import GUIConfig, WidgetGroupStateManager, apply_css_class
from .widgets import (
    AnimatedButtonGroup,
    APIKeyWidget,
    GenerationParametersWidget,
    PDFDropZone,
    PromptSelectorWidget,
    ResponsePanel,
)

if TYPE_CHECKING:
    from PyQt6.QtGui import QCloseEvent


# Mapping of model type strings to model classes
_MODEL_CLASSES = {
    "gemini": GeminiModel,
    "claude": ClaudeModel,
}


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
    prompt_path : str
        Path to the prompt markdown file.
    system_instruction_path : str | None
        Path to the system instruction file, or None.
    files : list of Path
        List of PDF file paths.
    json_schema_path : str | None
        Path to JSON schema file for structured output (Gemini only).
    generation_params : dict
        Generation parameters (temperature, top_p, top_k, max_tokens).
    """

    finished = pyqtSignal(str, bool)  # (response, success)
    error = pyqtSignal(str)

    def __init__(
        self,
        model_type: str,
        model_name: str,
        api_key: str,
        prompt_path: str,
        system_instruction_path: str | None,
        files: list[Path],
        json_schema_path: str | None,
        generation_params: dict,
    ) -> None:
        super().__init__()
        assert model_type in ("gemini", "claude")  # sanity-check
        self._model_type = model_type
        self._model_name = model_name
        self._api_key = api_key
        self._prompt_path = prompt_path
        self._system_instruction_path = system_instruction_path
        self._files = files
        self._json_schema_path = json_schema_path
        self._generation_params = generation_params

    def run(self) -> None:
        """Run the extraction in a background thread."""
        try:
            # Read system instruction content if path provided
            system_instruction = (
                read_markdown(self._system_instruction_path)
                if self._system_instruction_path
                else None
            )

            # Create model instance
            model_class = _MODEL_CLASSES[self._model_type]
            model = model_class(
                model_name=self._model_name,
                api_key=self._api_key,
                system_instruction=system_instruction,
                **self._generation_params,
            )

            # Query the model (Gemini supports json_schema, Claude does not)
            query_kwargs = {
                "prompt": self._prompt_path,
                "files": self._files if self._files else [],
            }
            if self._model_type == "gemini":
                query_kwargs["json_schema"] = self._json_schema_path
            response = model.query(**query_kwargs)

            self.finished.emit(response, True)

        except Exception as exc:
            self.error.emit(str(exc))
            self.finished.emit(str(exc), False)


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
        self._original_states: dict[str, bool] = {}

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

        # Main horizontal layout: config left, response right
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(*GUIConfig.WINDOW_MARGINS)
        main_layout.setSpacing(20)

        # === LEFT COLUMN: Configuration ===
        left_column = QWidget()
        left_column.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        left_column.setMinimumWidth(500)
        left_column.setMaximumWidth(600)
        left_layout = QVBoxLayout(left_column)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(GUIConfig.SECTION_SPACING)

        # --- Model Selection ---
        self._model_selector = AnimatedButtonGroup(["Gemini", "Claude"])
        left_layout.addWidget(self._model_selector)

        # --- Model Name Input ---
        model_name_section = QWidget()
        model_name_layout = QHBoxLayout(model_name_section)
        model_name_layout.setContentsMargins(0, 0, 0, 0)

        self._model_name_label = QLabel("Model:")
        self._model_name_label.setFixedWidth(80)
        model_name_layout.addWidget(self._model_name_label)

        self._model_name_input = QLineEdit()
        self._model_name_input.setPlaceholderText("Enter model name")
        model_name_layout.addWidget(self._model_name_input, 1)

        left_layout.addWidget(model_name_section)

        # --- API Key (no separator before) ---
        self._api_key_widget = APIKeyWidget()
        left_layout.addWidget(self._api_key_widget)

        # Separator
        left_layout.addWidget(self._create_separator())

        # --- System Instruction Selector ---
        self._system_selector = PromptSelectorWidget("system")
        left_layout.addWidget(self._system_selector)

        # --- Prompt Selector ---
        self._prompt_selector = PromptSelectorWidget("prompt")
        left_layout.addWidget(self._prompt_selector)

        # --- Generation Parameters ---
        params_section = QWidget()
        params_layout = QVBoxLayout(params_section)
        params_layout.setContentsMargins(0, 0, 0, 0)
        params_layout.setSpacing(5)

        self._params_label = QLabel("Generation Parameters")
        self._params_label.setProperty("class", "section-header")
        params_layout.addWidget(self._params_label)

        self._generation_params = GenerationParametersWidget()
        params_layout.addWidget(self._generation_params)

        left_layout.addWidget(params_section)

        # Separator
        left_layout.addWidget(self._create_separator())

        # --- PDF Drop Zone ---
        pdf_section = QWidget()
        pdf_layout = QVBoxLayout(pdf_section)
        pdf_layout.setContentsMargins(0, 0, 0, 0)

        self._pdf_label = QLabel("PDF Files (optional)")
        self._pdf_label.setProperty("class", "section-header")
        pdf_layout.addWidget(self._pdf_label)

        self._pdf_drop_zone = PDFDropZone()
        pdf_layout.addWidget(self._pdf_drop_zone)

        left_layout.addWidget(pdf_section)

        # Separator
        left_layout.addWidget(self._create_separator())

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
        left_layout.addWidget(run_section)

        # Spacer to push everything up
        left_layout.addStretch()

        main_layout.addWidget(left_column)

        # Vertical separator between columns
        v_separator = QFrame()
        v_separator.setFrameShape(QFrame.Shape.VLine)
        v_separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(v_separator)

        # === RIGHT COLUMN: Response ===
        right_column = QWidget()
        right_column.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self._response_panel = ResponsePanel()
        right_layout.addWidget(self._response_panel, 1)

        main_layout.addWidget(right_column, 1)

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
        # All input controls are disabled together during extraction
        self._widget_manager.register_group(
            "input-controls",
            [
                *self._model_selector.buttons,
                self._model_name_label,
                self._model_name_input,
                self._api_key_widget,
                self._system_selector,
                self._prompt_selector,
                self._params_label,
                self._generation_params,
                self._pdf_label,
                self._pdf_drop_zone,
                self._run_btn,
            ],
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
            and bool(self._model_name_input.text().strip())
        )
        self._run_btn.setEnabled(is_valid)

    def _on_run_clicked(self) -> None:
        """Handle run button click."""
        # Get model info (always valid - selector initialized at startup, no way to
        # deselect)
        model_type = self._model_selector.selected_label.lower()
        model_name = self._model_name_input.text().strip()
        api_key = self._api_key_widget.get_api_key()

        # Get prompt path (always valid - button disabled if invalid)
        prompt_path = self._prompt_selector.get_prompt_path()

        # Get system instruction path (optional)
        system_instruction_path = self._system_selector.get_prompt_path()

        # Get files
        files = self._pdf_drop_zone.get_files()

        # Get JSON schema path for Gemini
        json_schema_path = None
        if model_type == "gemini" and self._prompt_selector.has_json_schema():
            json_schema_path = self._prompt_selector.get_json_schema_path()

        # Get generation parameters
        generation_params = self._generation_params.get_parameters()

        # Disable UI during extraction
        self._set_running_state(True)

        # Start worker
        self._worker = ExtractionWorker(
            model_type=model_type,
            model_name=model_name,
            api_key=api_key,
            prompt_path=prompt_path,
            system_instruction_path=system_instruction_path,
            files=files,
            json_schema_path=json_schema_path,
            generation_params=generation_params,
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
