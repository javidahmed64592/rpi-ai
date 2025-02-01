from collections.abc import Callable


class FunctionsListBase:
    def __init__(self) -> None:
        self.functions: list[Callable] = []
