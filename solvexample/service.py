from sympy import *
from sympy.abc import *
from abc import ABC, abstractmethod

from .decorators import ToUserFriendlyAppearance


class AbstractMathOperations(ABC):
    @abstractmethod
    def solve_equation(self) -> str | dict | tuple:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...


class MathOperations(AbstractMathOperations):

    def __init__(self, example: str | list,
                 operation_type: str,
                 to_find: str = None) -> None:
        self.example = example
        self.to_find = to_find
        self.operation_type = operation_type
        self.__ARGS_VALIDATOR = [f'{to_find}*', f'*{to_find}', f'* {to_find}']

    @ToUserFriendlyAppearance.equations
    def solve_equation(self) -> str | dict | tuple | list:
        self.example = self.example.replace('=', '-')
        symbols_ = symbols(self.to_find)

        if self.operation_type == 'Система':
            try:
                solved_example: dict = solve(eval(self.example), symbols_).values()
            except NotImplementedError:
                solved_example: tuple = nsolve(eval(self.example), symbols_, [1, 1])
                solved_example = solved_example[0]

        elif self.operation_type == 'Система нерівностей':
            symbols_to_find = self.to_find.split(',')
            solved_example: list = []
            for single_symbol in symbols_to_find:
                solving = reduce_inequalities(eval(self.example), symbols(single_symbol))
                solved_example.append(solving)
            return solved_example

        elif self.operation_type == 'Похідна':
            expr = eval(self.example)
            solved_example: list = [simplify(expr.diff(eval(self.to_find[0])))]

        elif self.operation_type == 'Первісна':
            expr = eval(self.example)
            solved_example: list = [str(simplify(integrate(expr, eval(self.to_find), conds='none'))) + ' + C']

        else:
            symbol = Symbol(self.to_find)
            solved_example: str = solve(self.example, symbol)
            self.example = self.example.replace(' - ', ' = ')

        return solved_example

    def matrix(self):
        matrix_a = Matrix([eval(norm_v) for norm_v in
                          [fm.split(',\n') for fm in self.example][0]][0])

        matrix_b = Matrix([eval(norm_v) for norm_v in
                          [fm.split(',\n') for fm in self.example][1]][0])

        if self.operation_type in ['+', '-']:
            solved_example = eval(f'{matrix_a}{self.operation_type}{matrix_b}')

        elif self.operation_type == '*':
            solved_example = matrix_a.multiply(matrix_b)

        else:
            solved_example = None

        return eval(str(solved_example)[7: -1])

    def __str__(self) -> str:
        self.example = self.example.replace('**', '^')
        self.example = self.example.replace('sqrt', '√')

        for symbol in self.__ARGS_VALIDATOR:
            if symbol in self.example:
                self.example = self.example.replace('*', '')
        return self.example
