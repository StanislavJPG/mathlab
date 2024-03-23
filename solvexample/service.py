import functools
from typing import Callable

from sympy import And
from sympy.solvers import solve
from sympy.abc import *
from abc import ABC, abstractmethod


class AbstractMathOperations(ABC):
    @abstractmethod
    def solve_example(self) -> str | tuple:
        ...

    @staticmethod
    @abstractmethod
    def wrapper(func: Callable) -> Callable:
        ...

    @abstractmethod
    def read_example(self) -> str:
        ...


class MathOperations(AbstractMathOperations):

    def __init__(self, example: str,
                 to_find: str,
                 operation_type: str):
        self.example = example
        self.to_find = to_find
        self.operation_type = operation_type
        self.__VALIDATOR_ARGS = [f'{to_find}*', f'*{to_find}', f'{to_find} *', f'* {to_find}']

    @staticmethod
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrap(self) -> enumerate | str:
            if isinstance(func(self), And):
                return func(self)

            return enumerate(func(self), start=1)
        return wrap

    @wrapper
    def solve_example(self) -> str | tuple:
        self.example = self.example.replace('=', '-')

        if self.operation_type == 'Система':
            valid_args = self.to_find.split(',')
            symbols_ = symbols(valid_args)
            solved_example: tuple = solve(eval(self.example), symbols_)

        else:
            symbol = Symbol(self.to_find)
            solved_example: str = solve(self.example, symbol)
            self.example = self.example.replace('-', '=')

        return solved_example

    def read_example(self) -> str:
        self.example = self.example.replace('**', '^')
        self.example = self.example.replace('sqrt', '√')

        for symbol in self.__VALIDATOR_ARGS:
            if symbol in self.example:
                self.example = self.example.replace('*', '')
        return self.example
