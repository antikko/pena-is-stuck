"""GUI state commands."""
from enum import Enum, auto


class GUILayout(Enum):
    """Class representing a GUI state command."""

    CLOSE = auto()
    MENU = auto()
    MAZE = auto()
