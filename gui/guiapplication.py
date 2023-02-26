"""GUI module code."""
from typing import Any

from gui.gui_backend_interface import GUIBackendInterface
from gui.layouts.general import BaseLayout, LayoutParam
from gui.layouts.menu import Menu
from gui.layouts.maze import Maze
from gui.layouts.layoutoptions import GUILayout


class GUIApplication:  # pylint: disable=too-few-public-methods
    """GUI application."""

    def __init__(self, gui_backend_interface: GUIBackendInterface) -> None:
        """Initialize GUI application."""
        self._layouts = {
            GUILayout.MENU: Menu(gui_backend_interface),
            GUILayout.MAZE: Maze(gui_backend_interface),
        }
        self._current_layout: BaseLayout = self._layouts[GUILayout.MENU]

    def run(self) -> None:
        """Run GUI application."""
        param: LayoutParam[Any] | None = None
        while True:
            return_value = self._current_layout.run(param)
            if return_value.next_layout == GUILayout.CLOSE:
                break
            param = LayoutParam(
                return_value.value
            )
            self._current_layout = self._layouts[return_value.next_layout]
