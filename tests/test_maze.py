"""Maze related tests."""
import os
from unittest.mock import patch

from maze.maze import MazeFactory
from maze.mazeblock import BlockFactory, BlockIndex, BlockType


def test_maze_factory_creates_correct_maze_structure() -> None:
    data_to_block_type_map = {
        "#": BlockType.SOLID, "E": BlockType.EXIT, "^": BlockType.START, " ": BlockType.OPEN
    }

    block_factory = BlockFactory[str](data_to_block_type_map)
    maze_factory = MazeFactory(block_factory)
    with patch("fileparsing._DATA_DIR", os.path.join("tests", "data")):
        created_maze, start_block = maze_factory.create_maze("dummy_maze.txt")
        cb = block_factory.create_block
        expected_maze = [
            [cb("#", BlockIndex(0, 0)), cb("E", BlockIndex(0, 1)), cb("#", BlockIndex(0, 2))],
            [cb("^", BlockIndex(1, 0)), cb(" ", BlockIndex(1, 1)), cb("#", BlockIndex(1, 2))],
            [cb("#", BlockIndex(2, 0)), cb(" ", BlockIndex(2, 1)), cb("#", BlockIndex(2, 2))],
        ]
        assert len(created_maze) == len(expected_maze)
        for cr, er in zip(created_maze, expected_maze):
            assert len(cr) == len(er)
            for c, e in zip(cr, er):
                assert c.type_ == e.type_
                assert c.index == e.index

