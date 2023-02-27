"""Test GUI application basic functionality."""
# pylint: disable=all
from unittest.mock import patch

from gui.guiapplication import GUIApplication
from gui.layouts.general import LayoutReturnValue
from gui.layouts.layoutoptions import GUILayout


def test_guiapplication_handles_running_layouts() -> None:
    """Test GUI application starts."""
    mock_layout_data = []

    class MockLayout:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, *args, **kwargs):
            mock_layout_data.append("Called")

            return LayoutReturnValue(GUILayout.CLOSE, None)

    with patch("gui.guiapplication.Menu", MockLayout):
        gui_application = GUIApplication(None)
        gui_application.run()
        assert mock_layout_data == ["Called"]
