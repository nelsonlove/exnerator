from src.exnerator.enums import Card, DQ, Location, Determinant, FQ, ZScore, Special, Content
from src.exnerator import exceptions


def match(data, enum_):
    for member in enum_.__members__.values():
        if data == member.value:
            return member
    raise exceptions.CodeError(data, enum_)


def match_multiple(data, enum_, delimiter=','):
    if data == '' and 'NONE' in enum_.values():
        return enum_.NONE
    elif data == '':
        return set()
    return {match(datum, enum_) for datum in data.split(delimiter)}


def card(data):
    return match(data, Card)


def dq(data):
    data = data.lstrip('WDdS')
    return match(data, DQ)


def location(data):
    data = data.rstrip('+v/o')
    return match(data, Location)


def determinants(data):
    data = data.rstrip('+ou-').split('.')
    return [match(datum, Determinant) for datum in data]


def fq(data):
    if '.' in data:
        data = data.split('.')[-1]

    # Sort so that it looks for longer prefixes first
    for value in sorted(Determinant.values(), key=lambda c: len(c), reverse=True):
        if data.startswith(value):
            data = data[len(value):]
    return match(data, FQ)


def contents(data):
    return match_multiple(data, Content)


def z_score(data):
    return match(data, ZScore)


def special(data):
    return match_multiple(data, Special)
