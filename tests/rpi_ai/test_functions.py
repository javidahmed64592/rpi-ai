from rpi_ai.functions import FUNCTIONS
from rpi_ai.models.types import FunctionToolList


class TestFunctions:
    def test_check_functions(self) -> None:
        assert isinstance(FUNCTIONS, FunctionToolList)

    def test_check_functions_length(self) -> None:
        assert len(FUNCTIONS.functions) != 0
