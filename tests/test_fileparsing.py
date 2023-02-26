"""Tests related to fileparsing."""
import os
from unittest.mock import patch

import pytest

from fileparsing import MazeFileContext

_MAZE_FILE_DATA: list[str] = [
    "#######E########E####################",
    "# ### #   ###### #    #     #     # E",
    "# ### ### #      #  #    #     #    #",
    "# ### # # # ###### ##################",
    "#            #       #    #   #   # #",
    "#  # ##      # ##### #  # # # # # # #",
    "#  #         #   #   #  # # # # #   #",
    "#  ######   ###  #  ### # # # # ### #",
    "#  #    #               #   #   #   #",
    "#  # ## ########   ## ###########   #",
    "#    ##          ###                #",
    "# ## #############  ###   ####   ## #",
    "#  ### ##         #  #  #           #",
    "#  #   ## ####     #    #      ###  #",
    "#  # #### #  #     #    #####       #",
    "#  #      #      ###           ##   #",
    "#  #####           #   ##   #   #   #",
    "#                                   #",
    "##################^##################",
]


def test_read_maze_file() -> None:
    """Test maze file context manager by reading a maze file."""
    # Overwrite data dir for testing.
    with patch("fileparsing._DATA_DIR", os.path.join("tests", "data")):
        file_name = "maze-task-first.txt"
        with MazeFileContext(file_name) as file:
            for i, line in enumerate(file):
                assert _MAZE_FILE_DATA[i] == line


def test_file_not_found_raises() -> None:
    """Test maze file context manager raises FileNotFoundError."""
    with patch("fileparsing._DATA_DIR", os.path.join("tests", "data")):
        file_name = "this_file_is_not_found.txt"
        with pytest.raises(FileNotFoundError):
            with MazeFileContext(file_name):
                pass
