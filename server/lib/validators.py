from typing import List, Callable, Tuple


class Validator:
    def __init__(self, value: str):
        self.value = value
        self.checkers: List[Tuple[Callable, str]] = []

    def add(self, callback, message):
        self.checkers.append((callback, message))
        return self

    def check(self):
        for callback, message in self.checkers:
            if callback(self.value):
                raise ValueError(message)

        return self
