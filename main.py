"""Main program module."""
import functools

from fileparsing import get_maze_file_names
from gui.gui_backend_interface import GUIBackendInterface
from gui.guiapplication import GUIApplication
from maze.maze import Maze, MazeFactory
from maze.mazeblock import BlockFactory, BlockType
from maze.routefinder import bfs_search


def main() -> None:
    """Run program."""
    data_to_block_type_map = {
        "#": BlockType.SOLID, "E": BlockType.EXIT, "^": BlockType.START, " ": BlockType.OPEN
    }

    # Create factories and maze object.
    block_factory = BlockFactory[str](data_to_block_type_map)
    maze_factory = MazeFactory(block_factory)
    maze = Maze(maze_factory)

    # Create gui backend interface.
    gui_backend_interface = GUIBackendInterface(
        get_maze_file_names,
        maze,
    )

    # Create solver for maze.
    maze_solver = functools.partial(
        bfs_search,
        gui_hook_visited_block_index=gui_backend_interface.set_new_visited_blocks
    )

    # Add solver to maze.
    maze.solver = maze_solver

    # Create application and run.
    gui = GUIApplication(gui_backend_interface)
    gui.run()


if __name__ == "__main__":
    main()
