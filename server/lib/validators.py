class Validator:
    def __init__(self, value):
        self.value = value
        self.checkers = []

    def add(self, callback, message):
        self.checkers.append((callback, message))
        return self

    def check(self):
        for callback, message in self.checkers:
            if callback(self.value):
                raise ValueError(message)

        return self
