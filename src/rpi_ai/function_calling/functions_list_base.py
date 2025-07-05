from abc import ABC, abstractmethod
from collections.abc import Callable


class FunctionsListBase(ABC):
    def __init__(self) -> None:
        self.functions: list[Callable] = []
        self.setup_functions()

    @abstractmethod
    def setup_functions(self) -> None:
        pass
