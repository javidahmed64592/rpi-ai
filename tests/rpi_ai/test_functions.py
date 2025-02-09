from rpi_ai.functions import FUNCTIONS


class TestFunctions:
    def test_check_functions(self) -> None:
        assert isinstance(FUNCTIONS, list)
        assert len(FUNCTIONS) != 0
