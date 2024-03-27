from adrf.decorators import api_view
from django.shortcuts import render
from rest_framework.request import Request

from solvexample.service import MathOperations


@api_view()
def equations(request: Request):
    example = request.GET.get('example')
    to_find = request.GET.get('to-find')
    operation_type = request.GET.get('type')

    if example and to_find:
        math_solving = MathOperations(example, operation_type, to_find)
        result = math_solving.solve_equation()
        context = {
                    'solved_example': result,
                    'tofind': to_find,
                    'example': str(math_solving),
                    'type': operation_type
                   }
    else:
        context = {}

    return render(
        request=request,
        template_name='solvexample/equations.html',
        context=context
    )


def percents(request: Request):
    return render(request=request,
                  template_name='solvexample/percents.html')


def matrix(request: Request):
    matrix_a = request.GET.get('matrixA')
    matrix_b = request.GET.get('matrixB')
    operator = request.GET.get('operator')

    if matrix_a and matrix_b:
        matrix_solving = MathOperations(example=[matrix_a, matrix_b],
                                        operation_type=operator).matrix()
        context = {
                    'matrix_a': matrix_a,
                    'matrix_b': matrix_b,
                    'operator': operator,
                    'solved_example': matrix_solving
                  }
    else:
        context = {}

    return render(request=request,
                  template_name='solvexample/matrix.html',
                  context=context)
