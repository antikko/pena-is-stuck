"""GUI menu."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from gui.layouts.layoutoptions import GUILayout

T = TypeVar("T")


@dataclass
class LayoutReturnValue(Generic[T]):
    """A class representing layout return value."""

    next_layout: GUILayout
    value: T | None = None


class AbstractLayout(ABC):  # pylint: disable=too-few-public-methods
    """Abstract representation of a layout."""

    @abstractmethod
    def run(self) -> LayoutReturnValue[Any]:
        """Run layout."""
        raise NotImplementedError
