import re

from django.views.generic import TemplateView

from server.apps.solvexample.service import MathOperations


class MatricesTemplateView(TemplateView):
    template_name = 'partials/matrix.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matrix_a = f'[{self.request.GET.get("matrixA")}]'
        matrix_b = f'[{self.request.GET.get("matrixB")}]'
        operator = self.request.GET.get('operator')

        if eval(matrix_a)[0] and eval(matrix_b)[0]:
            matrices = []
            for single_matrix in [matrix_a, matrix_b]:
                matrices.append(list(eval(single_matrix.replace('\n', ''))))

            solved_example = MathOperations(example=matrices, operation_type=operator).solve_matrix()
            # expression pattern [x, y]
            pattern = r'\[([^\[\]]+),\s*([^\[\]]+)\]'

            # if the lookup expression is [x, y]:
            if re.match(pattern, str(solved_example)):
                solved_example = [solved_example]

            context.update(
                {
                    'matrix_a': eval(matrix_a),
                    'matrix_b': eval(matrix_b),
                    'operator': operator,
                    'solved_example': solved_example,
                }
            )
        return context
