import abc

import exceptions


class Code:
    codes = {}

    def __init__(self, value):
        self.value = self.match(value)

    @classmethod
    def index(cls, code):
        """Returns index value of code"""
        return list(cls.codes.keys()).index(code)

    @classmethod
    def lookup(cls, value):
        """Returns code for index value"""
        return list(cls.codes.keys())[value]

    @classmethod
    def lookup_multiple(cls, *values):
        return [cls.lookup(value) for value in values]

    def match(self, value):
        codes = list(self.codes.keys())
        if value not in codes:
            raise exceptions.DataException(codes, value)
        return codes.index(value)

    def __bool__(self):
        return bool(self.value)

    def __str__(self):
        return list(self.codes.keys())[self.value]


class SetCode(Code):
    delimiter = ','

    def __init__(self, value):
        super().__init__(value)

    def match(self, value):
        if not value:
            return set()
        values = value.split(self.delimiter)
        return {Code.match(self, v) for v in values}

    def __getitem__(self, item):
        return self.lookup(item)

    def __contains__(self, item):
        if type(item) is int:
            return item in self.value
        else:
            return item in [self.lookup(value) for value in self.value]

    def __str__(self):
        return self.delimiter.join(self.lookup(value) for value in self.value)
