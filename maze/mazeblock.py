"""Maze block related structures."""
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Generic, Self, TypeVar

BlockDataT = TypeVar("BlockDataT")


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
    START = "Start"
    EXIT = "Exit"
    SOLID = "Solid"


@dataclass
class MazeBlock:  # pylint: disable=too-many-instance-attributes
    """Class representing a single block of maze."""

    type_: BlockType
    index: BlockIndex
    visited: bool = False
    left: Self | None = None
    right: Self | None = None
    above: Self | None = None
    below: Self | None = None
    route_to_start: list["MazeBlock"] = field(default_factory=list)
    """Used for storing route to starting block when solving the maze."""

    def clear(self) -> None:
        """Clear block data."""
        self.visited = False
        self.route_to_start = []

    def next_available_blocks(self) -> list["MazeBlock"]:
        """Get next adjacent unvisited non-solid blocks."""
        available_blocks: list["MazeBlock"] = []
        if self.left is not None and self.left.type_ != BlockType.SOLID and not self.left.visited:
            available_blocks.append(self.left)
        if (
            self.right is not None
            and self.right.type_ != BlockType.SOLID
            and not self.right.visited
        ):
            available_blocks.append(self.right)
        if (
            self.above is not None
            and self.above.type_ != BlockType.SOLID
            and not self.above.visited
        ):
            available_blocks.append(self.above)
        if (
            self.below is not None
            and self.below.type_ != BlockType.SOLID
            and not self.below.visited
        ):
            available_blocks.append(self.below)

        return available_blocks

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


class BlockFactory(Generic[BlockDataT]):  # pylint: disable=too-few-public-methods
    """Class for creating blocks."""

    def __init__(self, data_to_block_type_map: dict[BlockDataT, BlockType]) -> None:
        """Initialize block factory."""
        self._data_to_block_type_map = data_to_block_type_map

    def create_block(self, data: BlockDataT, index: BlockIndex) -> MazeBlock:
        """Create a maze block from data."""
        return MazeBlock(
            type_=self._data_to_block_type_map[data],
            index=index,
        )
