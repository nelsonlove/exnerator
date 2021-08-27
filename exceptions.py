class DataException(ValueError):
    def __init__(self, expected, actual):
        self.actual = actual
        self.expected = expected

    def __str__(self):
        return f'Invalid data. Expected: {self.expected}. Actual: {repr(self.actual)}'
