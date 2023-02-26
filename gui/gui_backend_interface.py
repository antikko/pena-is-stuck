"""Interface between GUI and backend."""
from dataclasses import dataclass
from enum import StrEnum
from threading import Lock
from typing import Callable, Self

from maze.maze import Maze as BackendMaze
from maze.mazeblock import MazeBlock as BackendMazeBlock
from maze.mazeblock import BlockIndex, BlockType


@dataclass
class GUIMazeBlockIndex:
    """Class representing the position of GUIMazeBlock."""

    row: int
    column: int

    @classmethod
    def from_backend_block_index(cls, backend_block_index: BlockIndex) -> Self:
        """Get GUIMazeBlockIndex from backend maze block index."""
        return cls(
            backend_block_index.row,
            backend_block_index.column,
        )


class GUIMazeBlockType(StrEnum):
    """Class representing a gui maze bock type."""

    OPEN = "Open"
    START = "Start"
    EXIT = "Exit"
    SOLID = "Solid"

    @classmethod
    def from_backend_maze_block_type(cls, backend_block_type: BlockType) -> "GUIMazeBlockType":
        """Get GUIMazeBlockType from backend maze block type."""
        if backend_block_type == BlockType.OPEN:
            return cls.OPEN
        if backend_block_type == BlockType.START:
            return cls.START
        if backend_block_type == BlockType.EXIT:
            return cls.EXIT
        if backend_block_type == BlockType.SOLID:
            return cls.SOLID

        raise ValueError(f"Invalid backend block type '{backend_block_type}'.")


@dataclass
class GUIMazeBlock:
    """Class representing a maze block on GUI."""

    type_: GUIMazeBlockType
    index: GUIMazeBlockIndex
    visited: bool = False

    @classmethod
    def from_backend_maze_block(cls, backend_maze_block: BackendMazeBlock) -> Self:
        """Get GUIMazeBlock from backend maze block."""
        return cls(
            # pylint: disable=simplifiable-if-expression
            type_=GUIMazeBlockType.from_backend_maze_block_type(backend_maze_block.type_),
            # pylint: enable=simplifiable-if-expression
            index=GUIMazeBlockIndex.from_backend_block_index(backend_maze_block.index),
        )


class GUIBackendInterface:
    """Class representing an interface between GUI and backend."""

    def __init__(
        self,
        available_mazes: Callable[[], list[str]],
        maze: BackendMaze,
    ) -> None:
        """Initialize MazeDataInterface."""
        self._available_mazes = available_mazes
        self._backend_maze = maze
        self._threading_lock: Lock = Lock()
        self._new_visited_blocks_buffer: list[GUIMazeBlockIndex] = []

    def get_available_mazes_names(self) -> list[str]:
        """Get available mazes names from backend."""
        return self._available_mazes()

    def get_maze(self, name: str) -> list[list[GUIMazeBlock]]:
        """Get maze representation from backend."""
        self._backend_maze.create_maze(name)
        backend_maze_data = self._backend_maze.get_maze()
        gui_maze: list[list[GUIMazeBlock]] = []
        for row in backend_maze_data:
            gui_maze_row: list[GUIMazeBlock] = []
            for block in row:
                gui_maze_row.append(GUIMazeBlock.from_backend_maze_block(block))
            gui_maze.append(gui_maze_row)

        return gui_maze

    def solve_maze(self, max_route_length: int = 0, slow_down: bool = False) -> None:
        """Solve maze."""
        self._backend_maze.solve_maze(max_route_length, slow_down)

    def get_solved_route(self) -> list[GUIMazeBlockIndex] | None:
        """Get solved route in maze.

        None indicates there is no solution. Empty list indicates the solution has not been
        found yet.
        """
        solved_route = self._backend_maze.shortest_route
        if solved_route.blocks is None:
            return None
        if not solved_route:
            return []
        return [
            GUIMazeBlockIndex(block.index.row, block.index.column) for block in solved_route.blocks
        ]

    def get_new_visited_blocks(self) -> list[GUIMazeBlockIndex]:
        """Get new visited blocks from buffer."""
        with self._threading_lock:
            new_visited_blocks = self._new_visited_blocks_buffer.copy()
            self._new_visited_blocks_buffer.clear()
        return new_visited_blocks

    def set_new_visited_blocks(self, new_visited_blocks: list[BlockIndex]) -> None:
        """Set new visited blocks to buffer."""
        with self._threading_lock:
            self._new_visited_blocks_buffer += [
                GUIMazeBlockIndex(block.row, block.column) for block in new_visited_blocks
            ]
