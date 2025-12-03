"""Widget group state management singleton."""

from __future__ import annotations

import threading
import weakref
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


class WidgetGroupStateManager:
    """Singleton manager for controlling widget groups enabled/disabled states.

    This class manages groups of widgets that should be enabled/disabled together.
    It uses weak references to avoid keeping widgets alive longer than necessary.

    Notes
    -----
    Thread-safe implementation using RLock for all operations.
    """

    _instance: WidgetGroupStateManager | None = None
    _lock = threading.RLock()

    def __new__(cls) -> WidgetGroupStateManager:
        """Create or return the singleton instance.

        Returns
        -------
        WidgetGroupStateManager
            The singleton instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the state manager."""
        with self._lock:
            if not hasattr(self, "_groups"):
                self._groups: dict[str, list[weakref.ref]] = {}
            if not hasattr(self, "_group_states"):
                self._group_states: dict[str, bool] = {}

    def register_group(self, group_id: str, widgets: list[QWidget]) -> None:
        """Register a group of widgets that should be enabled/disabled together.

        Parameters
        ----------
        group_id : str
            Unique identifier for this widget group.
        widgets : list of QWidget
            List of widgets to include in this group.

        Notes
        -----
        Stores weak references to avoid keeping widgets alive.
        """
        if len(widgets) == 0:
            return
        with self._lock:
            self._groups[group_id] = [weakref.ref(widget) for widget in widgets]
            self._group_states[group_id] = True  # default to enabled

    def unregister_group(self, group_id: str) -> None:
        """Unregister a widget group.

        Parameters
        ----------
        group_id : str
            The group identifier to unregister.
        """
        with self._lock:
            self._groups.pop(group_id, None)
            self._group_states.pop(group_id, None)

    def set_group_enabled(self, group_id: str, enabled: bool) -> None:
        """Enable or disable a widget group.

        Parameters
        ----------
        group_id : str
            The group identifier.
        enabled : bool
            Whether to enable (True) or disable (False) the group.
        """
        with self._lock:
            if group_id not in self._groups:
                return

            self._group_states[group_id] = enabled
            widget_refs = self._groups[group_id]

            for widget_ref in widget_refs:
                widget = widget_ref()
                if widget is not None:
                    widget.setEnabled(enabled)
                    # Force style refresh to ensure CSS is reapplied
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)

    def is_group_enabled(self, group_id: str) -> bool:
        """Check if a widget group is enabled.

        Parameters
        ----------
        group_id : str
            The group identifier.

        Returns
        -------
        bool
            True if the group is enabled, False otherwise.
        """
        with self._lock:
            return self._group_states.get(group_id, True)

    def disable_all_groups(self) -> dict[str, bool]:
        """Disable all registered widget groups and return original states.

        Returns
        -------
        dict of str to bool
            Mapping of group IDs to their original enabled states.
        """
        with self._lock:
            original_states = self._group_states.copy()
            for group_id in self._group_states.keys():
                self.set_group_enabled(group_id, False)
            return original_states

    def restore_all_groups(self, original_states: dict[str, bool]) -> None:
        """Restore widget groups to their original enabled states.

        Parameters
        ----------
        original_states : dict of str to bool
            Mapping of group IDs to their original enabled states.
        """
        for group_id, original_enabled in original_states.items():
            self.set_group_enabled(group_id, original_enabled)

    def get_all_group_ids(self) -> list[str]:
        """Get all registered group IDs.

        Returns
        -------
        list of str
            List of all registered group identifiers.
        """
        with self._lock:
            return list(self._groups.keys())

    def clear_all(self) -> None:
        """Clear all registered groups.

        Notes
        -----
        Useful for cleanup during testing or application shutdown.
        """
        with self._lock:
            self._groups.clear()
            self._group_states.clear()

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance.

        Notes
        -----
        Primarily used for testing to ensure a clean state.
        """
        with cls._lock:
            if cls._instance is not None:
                cls._instance.clear_all()
            cls._instance = None
