import cmath
import random
from abc import abstractmethod
import operator
from typing import Callable, Any, Dict
from .field import FieldElement, ExtElement, getElement


def _to_constant(elem):
    if isinstance(elem, MapElementConstant):
        return elem.get_element()
    if isinstance(elem, int):
        return FieldElement(elem)
    if isinstance(elem, FieldElement):
        return elem
    return None


def wrap(elem):
    if isinstance(elem, MapElement):
        return elem
    if isinstance(elem, int) or isinstance(elem, FieldElement):
        return MapElementConstant(elem)
    return NotImplemented


def Convert(f):
    def wrapper(self, element):
        value = wrap(element)
        if (value == NotImplemented):
            return NotImplemented
        return f(self, value)

    return wrapper


class MapElement:

    @abstractmethod
    def __call__(self, variables: Dict) -> 'MapElement':
        pass

    def evaluate(self) -> FieldElement:
        map_elem = self.simplify()
        assert isinstance(map_elem, MapElementConstant)
        return map_elem.evaluate()

    def simplify(self) -> 'MapElement':
        return self

    @Convert
    def __add__(self, other):
        return _MapElementOp(self, other, operator.add).simplify()

    def __radd__(self, other):
        return self + other

    @Convert
    def __mul__(self, other):
        return _MapElementOp(self, other, operator.mul).simplify()

    def __rmul__(self, other):
        return self * other

    @Convert
    def __sub__(self, other):
        return _MapElementOp(self, other, operator.sub).simplify()

    @Convert
    def __rsub__(self, other):
        # After convert, other must be a MapElement
        return other - self

    @Convert
    def __truediv__(self, other):
        return _MapElementOp(self, other, operator.truediv).simplify()

    @Convert
    def __rtruediv__(self, other):
        # After convert, other must be a MapElement
        return other / self


class Var(MapElement):

    def __init__(self, name: str):
        self.name = name

    def __call__(self, variables: Dict) -> MapElement:
        return wrap(variables.get(self.name, self))


class UniMapping(MapElement):

    def __init__(self, uni_map, inside: MapElement):
        self.uni_map = uni_map
        self.inside = inside

    def __call__(self, variables) -> MapElement:
        if isinstance(variables, dict):
            inside = self.inside(variables)
            return UniMapping(self.uni_map, inside)
        if isinstance(self.inside, Var):
            wrapped = wrap(variables)
            if isinstance(wrapped, MapElement):
                return UniMapping(self.uni_map, wrapped)
        return NotImplemented

    def simplify(self) -> MapElement:
        inside = self.inside.simplify()
        return MapElementConstant(self.uni_map(inside.evaluate()))


class MapElementConstant(MapElement):

    def __init__(self, elem: ExtElement):
        self.elem = getElement(elem)

    def __call__(self, variables: Dict) -> MapElement:
        return self

    def evaluate(self) -> FieldElement:
        return self.elem

    def __add__(self, other):
        if isinstance(other, MapElementConstant):
            return MapElementConstant(self.get_element()+other.get_element())
        return NotImplemented()

    def __sub__(self, other):
        if isinstance(other, MapElementConstant):
            return MapElementConstant(self.get_element()-other.get_element())
        return NotImplemented()

    def __mul__(self, other):
        if isinstance(other, MapElementConstant):
            return MapElementConstant(self.get_element()*other.get_element())
        return NotImplemented()

    def __div__(self, other):
        if isinstance(other, MapElementConstant):
            return MapElementConstant(self.get_element()/other.get_element())
        return NotImplemented()


class _MapElementOp(MapElement):

    def __init__(
            self, map_elem_1: MapElement, map_elem_2: MapElement,
            op: Callable[[Any, Any], Any]):
        self.map_elem_1 = map_elem_1
        self.map_elem_2 = map_elem_2
        self.op = op

    def simplify(self):
        self.map_elem_1 = self.map_elem_1.simplify()
        self.map_elem_2 = self.map_elem_2.simplify()
        return self.op(self.map_elem_1, self.map_elem_2)

    def __call__(self, variables: Dict) -> MapElement:
        return self.op(self.map_elem_1(replace_mp), self.map_elem_2(replace_mp))


# class _MapElementAdd(MapElement):

#     def __init__(self, *elements):
#         self.map_elements = list(elements)

#     def simplify(self):
#         map_elements = []
#         constant = FieldElement(0)
#         for elem in self.map_elements:
#             elem = elem.simplify()
#             constant_elem = _to_constant(elem)
#             if constant_elem is not None:
#                 constant += constant_elem
#             else:
#                 map_elements.append(elem)
#         if len(map_elements) == 0:
#             return MapElementConstant(constant)
#         if constant != 0:
#             map_elements.append(MapElementConstant(constant))
#         return _MapElementAdd(map_elements)

#     def __call__(self, replace_mp: ReplaceMap) -> MapElement:
#         return _MapElementAdd(*[map_elem(replace_mp) for map_elem in self.map_elements]).simplify()

#     @Convert
#     def __add__(self, other):
#         if isinstance(other, _MapElementAdd):
#             return _MapElementAdd(self.map_elements + other.map_elements)
#         return _MapElementAdd(self.map_elements + [other])


# class _MapElementMult(MapElement):

#     def __init__(self, *elements):
#         self.map_elements = list(elements)

#     def simplify(self):
#         map_elements = []
#         constant = FieldElement(0)
#         for elem in self.map_elements:
#             elem = elem.simplify()
#             constant_elem = _to_constant(elem)
#             if constant_elem is not None:
#                 constant *= constant_elem
#             else:
#                 map_elements.append(elem)
#         if len(map_elements) == 0 or constant == 0:
#             return MapElementConstant(constant)

#         if constant != 1:
#             map_elements.append(MapElementConstant(constant))
#         return _MapElementMult(map_elements)

#     def __call__(self, replace_mp: ReplaceMap) -> MapElement:
#         return _MapElementMult(*[map_elem(replace_mp) for map_elem in self.map_elements])
