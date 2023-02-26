"""Route finder related code."""
import time
from typing import Callable
from maze.mazeblock import MazeBlock, BlockIndex, BlockType
from maze.maze import SolvedRoute


def bfs_search(
    start: MazeBlock,
    solved_route: SolvedRoute,
    max_length: int = 0,
    slow_down: bool = False,
    gui_hook_visited_block_index: Callable[[list[BlockIndex]], None] | None = None,
) -> None:
    """Breadth-first search for finding shortest route to exit.

    Args:
        start: Block to start from.
        max_length: Max length of the route to find. If 0 (default), find any length.
    """
    next_blocks = [start]
    current_block = start
    current_block.visited = True
    while next_blocks and (max_length == 0 or len(current_block.route_to_start) <= max_length):
        # Slow down for visualization of solving process if slow_down is set.
        if slow_down:
            time.sleep(0.01)

        current_block = next_blocks.pop(0)

        if gui_hook_visited_block_index is not None:
            if current_block.type_ == BlockType.OPEN:
                gui_hook_visited_block_index([current_block.index])

        next_available_blocks = current_block.next_available_blocks()
        # Add route to start info to next blocks and mark visited.
        for block in next_available_blocks:
            block.route_to_start += current_block.route_to_start + [current_block]
            block.visited = True

        next_blocks += next_available_blocks

        if current_block.type_ == BlockType.EXIT:
            solved_route.blocks = current_block.route_to_start
            return

    # No solution within step limits found.
    solved_route.blocks = None
