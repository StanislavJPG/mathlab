import re

from django.shortcuts import render
from rest_framework.request import Request

from server.apps.solvexample.service import MathOperations


def equations(request: Request):
    example = request.GET.get("example")
    to_find = request.GET.get("to-find")
    operation_type = request.GET.get("type")

    if operation_type:
        math_solving = MathOperations(example, operation_type, to_find)
        solved_example = math_solving.solve_equation()
        context = {
            "solved_example": solved_example,
            "tofind": to_find,
            "example": str(math_solving),
            "type": operation_type,
        }
    else:
        context = {}

    return render(
        request=request, template_name="solvexample/equations.html", context=context
    )


def percents(request: Request):
    example = request.GET.get("example")
    number = request.GET.get("num")
    percent = request.GET.get("percent")
    operation_type: str = request.GET.get("type")

    if operation_type:
        solved_example = MathOperations(
            example=[example, percent], to_find=number, operation_type=operation_type
        ).solve_percent()

        context = {
            "example": example,
            "number": number,
            "percent": percent,
            "solved_example": solved_example,
            "operation_type": operation_type,
        }
    else:
        context = {}

    return render(
        request=request, template_name="solvexample/percents.html", context=context
    )


def matrix(request: Request):
    matrix_a = f"[{request.GET.get('matrixA')}]"
    matrix_b = f"[{request.GET.get('matrixB')}]"
    operator = request.GET.get("operator")

    if eval(matrix_a)[0] and eval(matrix_b)[0]:
        matrices = []
        for single_matrix in [matrix_a, matrix_b]:
            matrices.append(list(eval(single_matrix.replace("\n", ""))))

        solved_example = MathOperations(
            example=matrices, operation_type=operator
        ).solve_matrix()
        # expression pattern [x, y]
        pattern = r"\[([^\[\]]+),\s*([^\[\]]+)\]"

        # if the lookup expression is [x, y]:
        if re.match(pattern, str(solved_example)):
            solved_example = [solved_example]

        context = {
            "matrix_a": eval(matrix_a),
            "matrix_b": eval(matrix_b),
            "operator": operator,
            "solved_example": solved_example,
        }
    else:
        context = {}

    return render(
        request=request, template_name="solvexample/matrix.html", context=context
    )
