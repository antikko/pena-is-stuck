"""Maze representation."""
from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable, Self


@dataclass
class BlockIndex:
    """Class representing block position in maze.

    This class makes it more convenient to inform the position to GUI.
    """

    row: int
    column: int


class BlockType(StrEnum):
    """Class representing a bock type."""

    OPEN = "Open"
    SOLID = "Solid"


@dataclass
class MazeBlock:
    """Class representing a single block of maze."""

    index: BlockIndex
    visited: bool = False
    left: Self | None = None
    right: Self | None = None
    above: Self | None = None
    below: Self | None = None

    def __str__(self) -> str:
        """Get string representation of MazeBlock.

        This custom string representation is created so the linked nature of the maze blocks
        won't prevent the use of a debugger.
        """
        return (
            f"visited: {self.visited}"
            f"index: {self.index}"
            f"left: {self.left.visited if self.left is not None else None}"
            f"right: {self.right.visited if self.right is not None else None}"
            f"above: {self.above.visited if self.above is not None else None}"
            f"below: {self.below.visited if self.below is not None else None}"
        )

    def __repr__(self) -> str:
        """Get repr of MazeBlock.

        This is same as the __str__ since there is no need to differentiate them in this case.
        """
        return str(self)


class Maze:
    """Class representing a maze."""

    def __init__(self, maze_data: Iterable[str], ) -> None:
        """Create maze."""
        self._blocks: list[list[MazeBlock]] = []
        self._create_maze(maze_data)

    def _create_maze(self, maze_data: Iterable[str]) -> list[list[MazeBlock]]:
        for row_data in maze_data:
            self._blocks.append(self._create_row(row_data))

    def _create_row(self, row_data: str) -> list[MazeBlock]:
        for 

