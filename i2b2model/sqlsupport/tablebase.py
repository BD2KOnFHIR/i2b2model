import inspect
from collections import OrderedDict
from typing import List, Callable, Union

from .orderedset import OrderedSet

EvalParam = Union[Callable[[object], object], Callable[[], object], object]


class ColumnsBase:
    """
    Base class for a dynamically evaluated columns list
    """
    _columns: OrderedSet = []

    @classmethod
    def _bind_keys(cls, keys: List[str]):
        for k in keys:
            if k not in cls._columns:
                cls._columns.add(k)

    def _freeze(self) -> OrderedDict:
        """
        Evaluate all of the column values and return the result
        :return: column/value tuples
        """
        return OrderedDict(**{k: getattr(self, k, None) for k in super().__getattribute__("_columns")})

    def _eval(self, m: EvalParam) -> object:
        """
        Evaluate m returning the method / function invocation or value.  Kind of like a static method
        :param m: object to evaluate
        :return: return
        """
        if inspect.ismethod(m) or inspect.isroutine(m):
            return m()
        elif inspect.isfunction(m):
            return m(self) if len(inspect.signature(m)) > 0 else m()
        else:
            return m

    def __getattribute__(self, item):
        if item.startswith("_"):
            return super().__getattribute__(item)
        cols = super().__getattribute__("_columns")
        if item in cols:
            return self._eval(super().__getattribute__(item))
        return super().__getattribute__(item)
