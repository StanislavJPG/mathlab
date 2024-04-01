from __future__ import annotations
import functools
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from solvexample.service import MathOperations


class ToUserFriendlyAppearance:
    @staticmethod
    def equations(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrap(self: MathOperations) -> list | dict:
            to_find = self.to_find.split(',')
            try:
                # index of arguments will be always 1
                # if quantity of unknown args greater than 1
                # (in system multiples args can not be repeated)
                if len(self.to_find) > 1:
                    return [
                        {
                            'key': 1,
                            'result': (to_find[kw], vw)
                         }
                        for kw, vw in enumerate(func(self))]

                # otherwise it's adding to the argument it's index
                # example: x1, x2
                # where 1 and 2 is kw + 1
                return [
                    {
                        'key': kw + 1,
                        'result': (to_find[0], vw)
                    }
                    for kw, vw in enumerate(func(self))]

            except TypeError:
                return func(self)

        return wrap

    @staticmethod
    def matrix(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrap(self: MathOperations) -> list:
            return eval(str(func(self))[8:-2])

        return wrap

    @staticmethod
    def percents(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrap(self: MathOperations) -> str:
            if self.operation_type == 'від числа x':
                return str(round(func(self), 3)) + '%'
            return func(self)

        return wrap
