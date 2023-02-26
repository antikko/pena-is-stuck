"""GUI module code."""
import PySimpleGUI as sg

from gui.layouts.general import AbstractLayout
from gui.layouts.menu import Menu
from gui.layouts.maze import Maze
from gui.layouts.layoutoptions import GUILayout


class GUIApplication:  # pylint: disable=too-few-public-methods
    """GUI application."""

    def __init__(self) -> None:
        """Initialize GUI application."""
        self._layouts = {
            GUILayout.MENU: Menu(),
            GUILayout.MAZE: Maze(),
        }
        self._current_layout: AbstractLayout = self._layouts[GUILayout.MENU]

    def run(self) -> None:
        """Run GUI application."""
        while True:
            return_value = self._current_layout.run()
            if return_value.next_layout == GUILayout.CLOSE:
                break
            self._current_layout = self._layouts[return_value.next_layout]
