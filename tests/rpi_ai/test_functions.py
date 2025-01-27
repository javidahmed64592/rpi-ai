from rpi_ai.functions import FUNCTIONS
from rpi_ai.models.types import FunctionsList


class TestFunctions:
    def test_check_functions(self) -> None:
        assert isinstance(FUNCTIONS, FunctionsList)

    def test_check_functions_length(self) -> None:
        assert len(FUNCTIONS.functions) != 0
