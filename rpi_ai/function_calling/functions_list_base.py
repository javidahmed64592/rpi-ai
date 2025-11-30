"""Base class for function lists in the RPi AI application."""

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator


class FunctionsListBase(ABC):
    """Abstract base class for function lists."""

    def __init__(self) -> None:
        """Initialise the function list."""
        self.functions: list[Callable] = []
        self.setup_functions()

    def __iter__(self) -> Iterator[Callable]:
        """Make the class iterable so list() returns the functions attribute.

        :return Iterator[Callable]:
            Iterator over functions
        """
        return iter(self.functions)

    @abstractmethod
    def setup_functions(self) -> None:
        """Set up the functions list."""
        pass
