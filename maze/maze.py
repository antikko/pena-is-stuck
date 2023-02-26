"""Maze representation."""
from dataclasses import dataclass
from threading import Thread
from typing import Callable, Iterable

from fileparsing import MazeFileContext
from maze.mazeblock import BlockFactory, BlockDataT, BlockIndex, BlockType, MazeBlock


class MazeFactory:  # pylint: disable=too-few-public-methods
    """Class for creating mazes from data."""

    def __init__(
        self,
        block_factory: BlockFactory[BlockDataT],
    ) -> None:
        """Initialize maze factory."""
        self._block_factory = block_factory
        self._blocks: list[list[MazeBlock]] = []
        self._start_block: MazeBlock | None = None

    def create_maze(self, maze_name: str) -> tuple[list[list[MazeBlock]], MazeBlock]:
        """Create maze data.

        Links automatically blocks while being created.

        Returns:
            A tuple containing a list of lists of MazeBlocks (the maze)
            and the start block for the maze.
        """
        with MazeFileContext(maze_name) as maze_file:
            self._create_rows(maze_file)
        maze = self._blocks.copy()
        self._blocks.clear()

        if self._start_block is None:
            raise ValueError("Invalid start block type 'None'.")

        return maze, self._start_block

    def _create_rows(self, maze_data: Iterable[Iterable[BlockDataT]]) -> None:
        """Create rows one by one."""
        for row_data in maze_data:
            self._blocks.append(self._create_row(row_data))

    def _create_row(self, row_data: Iterable[BlockDataT]) -> list[MazeBlock]:
        """Create a row block by block.

        Also link new blocks to old blocks while being created.
        """
        row_index = len(self._blocks)
        row: list[MazeBlock] = []
        for column_index, block_data in enumerate(row_data):
            block_above: MazeBlock | None = None
            block_left: MazeBlock | None = None

            if row_index > 0:
                block_above = self._blocks[row_index - 1][column_index]
            if column_index > 0:
                block_left = row[column_index - 1]

            block_index = BlockIndex(row_index, column_index)
            new_block = self._block_factory.create_block(block_data, block_index)

            if new_block.type_ == BlockType.START:
                self._start_block = new_block

            row.append(new_block)

            self._link_blocks(new_block, block_above, block_left)

        return row

    @staticmethod
    def _link_blocks(
        block: MazeBlock,
        above: MazeBlock | None,
        left: MazeBlock | None,
    ) -> None:
        if above is not None:
            block.above = above
            above.below = block
        if left is not None:
            block.left = left
            left.right = block


@dataclass
class SolvedRoute:
    """Class representing a solved route in maze.

    None indicates that there is no solution available. Empty list indicates that route has not yet
    been solved.
    """

    blocks: list[MazeBlock] | None


class Maze:  # pylint: disable=too-few-public-methods
    """Class representing a maze."""

    def __init__(
        self,
        maze_factory: MazeFactory,
        solver: Callable[[MazeBlock, int], list[MazeBlock] | None] | None = None,
    ) -> None:
        """Create maze."""
        self._maze_factory = maze_factory
        self._blocks: list[list[MazeBlock]] = []
        self._start_block: MazeBlock | None
        self.solver = solver
        self.shortest_route = SolvedRoute([])
        self._solver_has_been_running = False

    def create_maze(self, maze_name: str) -> None:
        """Create maze from data."""
        self._blocks, self._start_block = self._maze_factory.create_maze(maze_name)

    def get_maze(self) -> list[list[MazeBlock]]:
        """Get created maze data structure."""
        return self._blocks

    def solve_maze(self, max_route_length: int = 0, slow_down: bool = False) -> None:
        """Solve maze finding shortest route from start to exit.

        Args:
            max_length: Max length of the route to find. If 0 (default), find any length.
        Returns:
            List of MazeBlocks or None if no route was found.
        """
        if self._solver_has_been_running:
            self._clear()
        if self.solver is None:
            raise ValueError("Solver not found.")
        if not self._blocks:
            raise ValueError("Could not solve the maze. Empty maze is not valid.")
        if self._start_block is None:
            raise ValueError("Start block type 'None' invalid.")

        self._solver_has_been_running = True
        solver_thread = Thread(
            target=self.solver,
            args=(self._start_block, self.shortest_route, max_route_length, slow_down)
        )
        solver_thread.start()

    def _clear(self) -> None:
        self.shortest_route.blocks = []
        for row in self._blocks:
            for block in row:
                block.clear()
        self._solver_has_been_running = False
