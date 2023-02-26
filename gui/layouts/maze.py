"""Maze layout."""
from enum import StrEnum
from typing import Any

import PySimpleGUI as sg

from gui.layouts.general import AbstractLayout, LayoutReturnValue
from gui.layouts.layoutoptions import GUILayout


class _Event(StrEnum):
    """Class representing an event from GUI."""

    BACK_TO_MENU = "Menu"
    EXIT = "Exit"


class _Keys(StrEnum):
    """Class representing keys of GUI elements."""

    MAZE_SELECTION = "maze_selection"
    MENU_TEXT = "menu_text"


class Maze(AbstractLayout):  # pylint: disable=too-few-public-methods
    """Maze layout."""

    def __init__(self):
        """Initialize maze layout."""
        super().__init__()

    def run(self) -> LayoutReturnValue[None]:
        """Run menu."""
        layout = self._create_layout()
        window = sg.Window("Pena Stuck In a Maze - Maze", layout)
        while True:
            event, _ = window.read()
            if event in (sg.WIN_CLOSED, _Event.EXIT):
                window.close()
                return LayoutReturnValue(GUILayout.CLOSE)
            if event == _Event.BACK_TO_MENU:
                window.close()
                return LayoutReturnValue(GUILayout.MENU)

    def _create_layout(self) -> list[Any]:
        """Create maze layout.

        Because of PySimpleGUI typing, the return list parameters are difficult to annotate better.
        However, the list contains PySimpleGUI elements and other lists.
        """
        return [
            [sg.Graph(
                canvas_size=(1000, 1000),
                graph_bottom_left=(-500, -500),
                graph_top_right=(500, 500),
                key="graph",
            )],
            [sg.Button(_Event.BACK_TO_MENU), sg.Button(_Event.EXIT)],
        ]
