"""MazeBlock related tests."""
import pytest
from maze.mazeblock import BlockType, BlockFactory, MazeBlock, BlockIndex


def test_maze_block_factory() -> None:
    data_to_block_type_map = {
        "#": BlockType.SOLID, "E": BlockType.EXIT, "^": BlockType.START, " ": BlockType.OPEN
    }
    factory = BlockFactory[str](data_to_block_type_map)
    assert factory.create_block("#", BlockIndex(0, 0)) == MazeBlock(
        BlockType.SOLID, BlockIndex(0, 0)
    )
    assert factory.create_block("E", BlockIndex(0, 0)) == MazeBlock(
        BlockType.EXIT, BlockIndex(0, 0)
    )
    assert factory.create_block("^", BlockIndex(0, 0)) == MazeBlock(
        BlockType.START, BlockIndex(0, 0)
    )
    assert factory.create_block(" ", BlockIndex(0, 0)) == MazeBlock(
        BlockType.OPEN, BlockIndex(0, 0)
    )


def test_maze_block_factory_key_error_for_invalid_block_data() -> None:
    data_to_block_type_map = {
        "#": BlockType.SOLID, "E": BlockType.EXIT, "^": BlockType.START, " ": BlockType.OPEN
    }
    factory = BlockFactory[str](data_to_block_type_map)
    with pytest.raises(KeyError):
        factory.create_block("A", BlockIndex(0, 0))


def test_maze_block_returns_correct_next_blocks() -> None:
    data_to_block_type_map = {
        "#": BlockType.SOLID, "E": BlockType.EXIT, "^": BlockType.START, " ": BlockType.OPEN
    }
    factory = BlockFactory[str](data_to_block_type_map)
    block1 = factory.create_block(" ", BlockIndex(0, 0))
    block2 = factory.create_block(" ", BlockIndex(0, 0))
    block3 = factory.create_block(" ", BlockIndex(0, 0))
    block4 = factory.create_block("#", BlockIndex(0, 0))
    block5 = factory.create_block(" ", BlockIndex(0, 0))
    block1.left = block2
    block2.right = block1
    block1.above = block3
    block3.below = block1
    block1.right = block4
    block4.left = block1
    block1.below = block5
    block5.above = block1
    assert block1.next_available_blocks() == [block2, block3, block5]


def test_maze_block_returns_correct_next_blocks_when_some_visited() -> None:
    data_to_block_type_map = {
        "#": BlockType.SOLID, "E": BlockType.EXIT, "^": BlockType.START, " ": BlockType.OPEN
    }
    factory = BlockFactory[str](data_to_block_type_map)
    block1 = factory.create_block(" ", BlockIndex(0, 0))
    block2 = factory.create_block(" ", BlockIndex(0, 0))
    block3 = factory.create_block(" ", BlockIndex(0, 0))
    block4 = factory.create_block("#", BlockIndex(0, 0))
    block1.left = block2
    block2.right = block1
    block1.above = block3
    block3.below = block1
    block1.right = block4
    block4.left = block1
    block2.visited = True
    assert block1.next_available_blocks() == [block3]
