from adrf.decorators import api_view
from django.shortcuts import render
from rest_framework.request import Request

from solvexample.service import MathOperations


@api_view()
def index(request: Request):
    example = request.GET.get('example')
    to_find = request.GET.get('to-find')
    operation_type = request.GET.get('type')

    math_solving = MathOperations(example, to_find, operation_type)

    if example and to_find:
        result = math_solving.solve_example()
        example = math_solving.read_example()

        return render(
            request=request,
            template_name='solvexample/index.html',
            context={'solved_example': result,
                     'tofind': to_find,
                     'example': example,
                     'type': operation_type}
        )
    else:
        return render(
            request=request,
            template_name='solvexample/index.html',
        )
