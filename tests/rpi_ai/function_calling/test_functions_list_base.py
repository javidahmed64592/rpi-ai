from collections.abc import Callable

from rpi_ai.function_calling.functions_list_base import FunctionsListBase


class TestFunctionsListBase:
    def test_initialization(self) -> None:
        flb = FunctionsListBase()
        assert isinstance(flb.functions, list)
        assert len(flb.functions) == 0

    def test_add_function(self) -> None:
        flb = FunctionsListBase()

        def dummy_function() -> str:
            return "dummy"

        flb.functions.append(dummy_function)
        assert len(flb.functions) == 1
        assert isinstance(flb.functions[0], Callable)
        assert flb.functions[0]() == "dummy"

    def test_remove_function(self) -> None:
        flb = FunctionsListBase()

        def dummy_function() -> str:
            return "dummy"

        flb.functions.append(dummy_function)
        flb.functions.remove(dummy_function)
        assert len(flb.functions) == 0

    def test_clear_functions(self) -> None:
        flb = FunctionsListBase()

        def dummy_function() -> str:
            return "dummy"

        flb.functions.append(dummy_function)
        flb.functions.clear()
        assert len(flb.functions) == 0
