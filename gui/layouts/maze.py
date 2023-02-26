"""Maze layout."""
from enum import StrEnum
from typing import Any

import PySimpleGUI as sg

from gui.gui_backend_interface import GUIMazeBlock, GUIMazeBlockIndex, GUIMazeBlockType
from gui.layouts.general import BaseLayout, LayoutParam, LayoutReturnValue
from gui.layouts.layoutoptions import GUILayout


class _Event(StrEnum):
    """Class representing an event from GUI."""

    BACK_TO_MENU = "Menu"
    SOLVE_MAZE = "Find Shortest Route"
    EXIT = "Exit"


class _Keys(StrEnum):
    """Class representing keys of GUI elements."""

    MAZE_SELECTION = "maze_selection"
    MENU_TEXT = "menu_text"
    GRAPH = "graph"
    INFO_TEXT = "info_text"
    DROP_DOWN_TITLE = "drop_down_title"
    DROP_DOWN = "drop_down"
    SLOW_DOWN = "slow_down"


class Maze(BaseLayout):  # pylint: disable=too-few-public-methods
    """Maze layout."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize maze layout."""
        super().__init__(*args, **kwargs)
        self._maze: list[list[GUIMazeBlock]] = []
        self._block_size: int = 20
        self._graph: sg.Graph | None = None
        self._solver_has_been_running = False

    def run(self, param: LayoutParam[str] | None) -> LayoutReturnValue[None]:
        """Run menu."""
        self._solver_has_been_running = False
        if param is None or (maze_selection := param.value) is None:
            raise ValueError("Invalid maze selection.")

        self._maze = self._gui_backend_interface.get_maze(maze_selection)
        layout = self._create_layout()
        window = sg.Window("Pena Stuck In a Maze - Maze", layout, grab_anywhere=True, finalize=True)
        self._draw_blocks()

        solving_maze = False
        while True:
            event, values = window.read(timeout=0)
            if event in (sg.WIN_CLOSED, _Event.EXIT):
                window.close()
                return LayoutReturnValue(GUILayout.CLOSE)
            if event == _Event.BACK_TO_MENU:
                window.close()
                return LayoutReturnValue(GUILayout.MENU)
            if event == _Event.SOLVE_MAZE and not solving_maze:
                # Clear maze if solver has been running before.
                if self._solver_has_been_running:
                    self._draw_blocks()
                self._solver_has_been_running = True
                if (step_limit := values[_Keys.DROP_DOWN]):
                    self._gui_backend_interface.solve_maze(step_limit, values[_Keys.SLOW_DOWN])
                else:
                    self._gui_backend_interface.solve_maze(slow_down=values[_Keys.SLOW_DOWN])
                solving_maze = True
            elif solving_maze:
                solved_route = self._gui_backend_interface.get_solved_route()
                # No solution to maze found.
                if solved_route is None:
                    solving_maze = False
                    window[_Keys.INFO_TEXT].update("Solution to maze not found.")
                # Maze not yet solved if solved route empty.
                elif solved_route:
                    solving_maze = False
                    self._draw_solved_route(solved_route)
                    window[_Keys.INFO_TEXT].update(
                        f"Maze solved! Shortest route length: {len(solved_route)}"
                    )

            self._update_visited_blocks(self._gui_backend_interface.get_new_visited_blocks())

    def _draw_solved_route(self, solved_route: list[GUIMazeBlockIndex]) -> None:
        if self._graph is None:
            raise ValueError("Graph does not exist. Could not draw solved route.")

        for index in solved_route:
            self._graph.draw_rectangle(
                (self._block_size * index.column, self._block_size * index.row),
                (
                    self._block_size * index.column + self._block_size,
                    self._block_size * index.row + self._block_size
                ),
                fill_color="blue",
            )

    def _update_visited_blocks(self, block_indices: list[GUIMazeBlockIndex]) -> None:
        if self._graph is None:
            raise ValueError("Graph does not exist. Could not draw visited blocks.")
        for index in block_indices:
            self._graph.draw_rectangle(
                (self._block_size * index.column, self._block_size * index.row),
                (
                    self._block_size * index.column + self._block_size,
                    self._block_size * index.row + self._block_size
                ),
                fill_color="yellow",
            )

    def _draw_blocks(self) -> None:
        if self._graph is None:
            raise ValueError("Graph does not exist. Could not draw blocks.")
        for row in self._maze:
            for block in row:
                color = "black"
                if block.type_ == GUIMazeBlockType.START:
                    color = "red"
                elif block.type_ == GUIMazeBlockType.EXIT:
                    color = "green"
                elif block.type_ == GUIMazeBlockType.OPEN:
                    color = "white"
                self._graph.draw_rectangle(
                    (self._block_size * block.index.column, self._block_size * block.index.row),
                    (
                        self._block_size * block.index.column + self._block_size,
                        self._block_size * block.index.row + self._block_size
                    ),
                    fill_color=color
                )

    def _create_layout(self) -> list[Any]:
        """Create maze layout.

        Because of PySimpleGUI typing, the return list parameters are difficult to annotate better.
        However, the list contains PySimpleGUI elements and other lists.
        """
        canvas_size = (len(self._maze[0])*self._block_size, len(self._maze)*self._block_size)
        graph_top_right = (canvas_size[0], 0)
        graph_bottom_left = (0, canvas_size[1])
        self._graph = sg.Graph(
            canvas_size=canvas_size,
            graph_bottom_left=graph_bottom_left,
            graph_top_right=graph_top_right,
            key=_Keys.GRAPH,
        )
        return [
            [self._graph],
            [
                sg.Text("Step Limit: ", key=_Keys.DROP_DOWN_TITLE),
                sg.DropDown([20, 150, 200], key=_Keys.DROP_DOWN),
                sg.Checkbox("Slow Down Solver For Animation", key=_Keys.SLOW_DOWN),
                sg.Button(_Event.SOLVE_MAZE),
                sg.Button(_Event.BACK_TO_MENU),
                sg.Button(_Event.EXIT),
                sg.Text(key=_Keys.INFO_TEXT)
            ],
        ]
