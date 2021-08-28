import abc


class DataException(ValueError):
    def __init__(self, expected, actual):
        self.actual = actual
        self.expected = expected

    def __str__(self):
        return f'Invalid data. Expected: {self.expected}. Actual: {repr(self.actual)}'


class CodeError(Exception):
    def __init__(self, value, enum_):
        self.value = value
        self.enum = enum_

    def __str__(self):
        return f'Invalid code. Expected: {self.enum.values()}. Actual: {repr(self.value)}'


class FileError(Exception, metaclass=abc.ABCMeta):
    def __init__(self, file):
        self.file = file

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError


class InvalidColumnsError(FileError):
    def __str__(self):
        return f'Active sheet in {self.file} has {self.file.columns} columns; expected 9.'


class NoResponsesError(FileError):
    def __str__(self):
        return f'Active sheet in {self.file} has no responses.'
