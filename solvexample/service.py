from sympy import *
from sympy.abc import *

from .decorators import ToUserFriendlyAppearance
from typing import Union


class MathOperations:

    def __init__(self, example: str | list,
                 operation_type: str = None,
                 to_find: str | int | float = None) -> None:
        self.example = example
        self.to_find = to_find
        self.operation_type = operation_type
        self.__ARGS_VALIDATOR = [f'{to_find}*', f'*{to_find}', f'* {to_find}']

    @ToUserFriendlyAppearance.equations
    def solve_equation(self) -> Union[str, dict, tuple, list]:
        self.example = self.example.replace('=', '-')
        symbols_ = symbols(self.to_find)

        if self.operation_type == 'Система':
            try:
                solved_equation: dict = solve(eval(self.example), symbols_).values()
            except NotImplementedError:
                solved_equation: tuple = nsolve(eval(self.example), symbols_, [1, 1])
                solved_equation = solved_equation[0]

        elif self.operation_type == 'Система нерівностей':
            symbols_to_find = self.to_find.split(',')
            solved_equation: list = []
            for single_symbol in symbols_to_find:
                solving = reduce_inequalities(eval(self.example), symbols(single_symbol))
                solved_equation.append(solving)
            return solved_equation

        elif self.operation_type == 'Похідна':
            expr = eval(self.example)
            solved_equation: list = [simplify(expr.diff(eval(self.to_find[0])))]

        elif self.operation_type == 'Первісна':
            expr = eval(self.example)
            solved_equation: list = [str(simplify(integrate(expr, eval(self.to_find), conds='none'))) + ' + C']

        else:
            to_find = self.to_find
            symbol = tuple(Symbol(sym) for sym in to_find.split(','))
            solved_equation: str = solve(self.example, *symbol)
            self.example = self.example.replace('-', ' = ')

        return solved_equation

    @ToUserFriendlyAppearance.matrix
    def solve_matrix(self) -> MutableDenseMatrix:
        matrix_a = Matrix(self.example[0])
        matrix_b = Matrix(self.example[1])

        if len(matrix_a) == 1:
            matrix_a = self.example[0]

        if len(matrix_b) == 1:
            matrix_b = self.example[1][0]

        solved_example = eval(f'{matrix_a}{self.operation_type}{matrix_b}')

        return solved_example

    @ToUserFriendlyAppearance.percents
    def solve_percent(self) -> float:
        try:
            # replace % with '' if user wrote number like so
            self.example[1] = self.example[1].replace('%', '')
            if self.operation_type == 'від числа x':
                return (float(self.to_find) * float(self.example[1])) / float(self.example[0])

            # otherwise it calculates number from percent
            return (float(self.example[0]) / 100) * float(self.example[1])
        except ValueError:
            raise ValueError('Must be a valid arguments')

    def __str__(self) -> str:
        self.example = self.example.replace('**', '^')
        self.example = self.example.replace('sqrt', '√')

        for symbol in self.__ARGS_VALIDATOR:
            if symbol in self.example:
                self.example = self.example.replace('*', '')
        return self.example
