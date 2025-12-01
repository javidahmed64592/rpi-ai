"""Unit tests for the rpi_ai.functions module."""

from rpi_ai.functions import FUNCTIONS


class TestFunctions:
    """Tests for the FUNCTIONS list in the rpi_ai.functions module."""

    def test_check_functions(self) -> None:
        """Test that FUNCTIONS is a non-empty list."""
        assert isinstance(FUNCTIONS, list)
        assert len(FUNCTIONS) != 0
