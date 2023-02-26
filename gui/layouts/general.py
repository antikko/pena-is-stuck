"""GUI menu."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from gui.gui_backend_interface import GUIBackendInterface
from gui.layouts.layoutoptions import GUILayout

T = TypeVar("T")
ParamT = TypeVar("ParamT")


@dataclass
class LayoutReturnValue(Generic[T]):
    """A class representing layout return value."""

    next_layout: GUILayout
    value: T | None = None


@dataclass
class LayoutParam(Generic[ParamT]):
    """A class representing layout parameter."""

    value: ParamT | None = None


class BaseLayout(ABC):  # pylint: disable=too-few-public-methods
    """Base representation of a layout."""

    def __init__(self, gui_backend_interface: GUIBackendInterface) -> None:
        """Initialize BaseLayout."""
        self._gui_backend_interface = gui_backend_interface

    @abstractmethod
    def run(self, param: LayoutParam[Any] | None) -> LayoutReturnValue[Any]:
        """Run layout."""
        raise NotImplementedError
