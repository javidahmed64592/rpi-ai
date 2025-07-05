from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator


class FunctionsListBase(ABC):
    def __init__(self) -> None:
        self.functions: list[Callable] = []
        self.setup_functions()

    def __iter__(self) -> Iterator[Callable]:
        """Make the class iterable so list() returns the functions attribute."""
        return iter(self.functions)

    @abstractmethod
    def setup_functions(self) -> None:
        pass
