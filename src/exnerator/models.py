import abc
from enum import Enum


class CodeEnum(Enum):
    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]


class File(metaclass=abc.ABCMeta):
    def __init__(self, filename):
        self.filename = filename
        print(f'Loading {self}...', sep='')
        self._data = self.open()
        self.validate()

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def open(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def columns(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def responses(self):
        raise NotImplementedError

    @abc.abstractmethod
    def validate(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def data(self):
        raise NotImplementedError


