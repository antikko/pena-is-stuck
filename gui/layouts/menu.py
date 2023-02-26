"""Menu layout."""
from enum import StrEnum
from typing import Any

import PySimpleGUI as sg

from fileparsing import get_maze_file_names
from gui.layouts.general import AbstractLayout, LayoutReturnValue
from gui.layouts.layoutoptions import GUILayout


class _Event(StrEnum):
    """Class representing an event from GUI."""

    OPEN_MAZE = "Open Maze"
    EXIT = "Exit"


class _Keys(StrEnum):
    """Class representing keys of GUI elements."""

    MAZE_SELECTION = "maze_selection"
    MENU_TEXT = "menu_text"


class Menu(AbstractLayout):  # pylint: disable=too-few-public-methods
    """Menu layout."""

    def __init__(self):
        """Initialize menu layout factory."""
        super().__init__()
        self._maze_names = get_maze_file_names()

    def run(self) -> LayoutReturnValue[str]:
        """Run menu."""
        layout = self._create_layout()
        window = sg.Window("Pena Stuck In a Maze - Menu", layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, _Event.EXIT):
                window.close()
                return LayoutReturnValue(GUILayout.CLOSE)
            if event == _Event.OPEN_MAZE:
                if (selection := values[_Keys.MAZE_SELECTION]) not in self._maze_names:
                    continue
                window.close()
                return LayoutReturnValue(
                    GUILayout.MAZE,
                    str(selection),
                )

    def _create_layout(self) -> list[Any]:
        """Create menu layout.

        Because of PySimpleGUI typing, the return list parameters are difficult to annotate better.
        However, the list contains PySimpleGUI elements and other lists.
        """
        return [
            [sg.Text("Select Maze", key=_Keys.MENU_TEXT)],
            [sg.DropDown(self._maze_names, key=_Keys.MAZE_SELECTION)],
            [sg.Button(_Event.OPEN_MAZE)],
            [sg.Button(_Event.EXIT)],
        ]
