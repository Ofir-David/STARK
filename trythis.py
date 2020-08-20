import pytest
import inspect

from marshmallow_dataclass import dataclass as m_dataclass
import marshmallow_dataclass
import dataclasses

'''
def bar():
    print("hello")


print(type(bar))


def foo(f):
    def wrapper(*arg):
        print('hi')
        f(*arg)
        print('bye')
    return wrapper


@foo
@pytest.mark.parametrized('a', [1, 2, 3])
def test_me(a):
    assert a > 0
'''

'''
@pytest.mark.parametrized('a', [1, 2, 3])
def test(a):
    assert a == 0


print(test.__code__.co_varnames)
'''


@m_dataclass
class Data:
    suit: str
    rank: str


d = Data("hearts", "4")
md = dataclasses.replace(d, **{"suit": "club"})
cls = d.__class__
dtemp = cls(**d.__dict__)
dtemp.rank = "10"
dd = d
ddd = Data(**d.__dict__)
print(d)
dd.suit = "diamond"
print(d)
print(dd)
print(ddd)
print(dtemp)
print(md)

# I added a new feature
# another feature

'''from .enumTest import Enum, auto


def printAll(enumCls):
    print(enumCls.__name__)
    for data in enumCls:
        print(f'    - {data.name}: {data.value}')
    print('--------------------------\n')


class option1(Enum):
    cat = 0
    dog = auto()
    mouse = auto()
    rabbit = 5
    horse = auto()
    sheep = auto()
    cow = auto()
    pig = 7
    fish = auto()


printAll(option1)


class Enum0(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count


class option2(Enum0):
    cat = auto()
    dog = auto()
    mouse = auto()
    rabbit = 5
    horse = auto()
    sheep = auto()
    cow = auto()
    pig = 7
    fish = auto()


printAll(option2)


class Enum00(Enum):
    def _generate_next_value_(name, start, count, last_values):
        for last_value in reversed(last_values):
            try:
                return last_value + 1
            except TypeError:
                pass
        else:
            return 0


class option3(Enum00):
    cat = auto()
    dog = auto()
    mouse = auto()
    rabbit = 5
    horse = auto()
    sheep = auto()
    cow = auto()
    pig = 7
    fish = auto()


printAll(option3)'''
