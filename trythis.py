from .enumTest import Enum, auto


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


printAll(option3)
