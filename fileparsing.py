"""File parsing related code."""
import os

from types import TracebackType
from typing import Generator

_DATA_DIR: str = "data"


def get_maze_file_names() -> list[str]:
    """Get maze file names in data dir."""
    return os.listdir(_DATA_DIR)


class MazeFileContext:
    """File reader context for the maze file.

    This context manager is used for reading maze files from data dir. Includes automatic checking
    that the file exists.
    """

    def __init__(self, file_name: str):
        """Create a context manager for maze file.

        Args:
            file_name: Name of the file in data folder.

        Raises:
            FileNotFoundError: Specified file not found.
        """
        file_path = os.path.join(_DATA_DIR, file_name)

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_name} not found!")

        # pylint: disable=consider-using-with
        self.file_object = open(file_path, "r", encoding="utf-8")
        # pylint: enable=consider-using-with

    def __enter__(self) -> Generator[str, None, None]:
        """Read maze file from data folder line by line.

        Returns:
            A generator of lines as strings.
        """
        return (line.rstrip() for line in self.file_object)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context and close the file."""
        self.file_object.close()
