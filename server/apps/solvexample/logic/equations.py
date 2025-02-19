from django.views.generic import TemplateView

from server.apps.solvexample.service import MathOperations


class EquationsTemplateView(TemplateView):
    template_name = "partials/equations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        example = self.request.GET.get("example")
        to_find = self.request.GET.get("to-find")
        operation_type = self.request.GET.get("type")

        if operation_type:
            math_solving = MathOperations(example, operation_type, to_find)
            solved_example = math_solving.solve_equation()
            context.update(
                {
                    "solved_example": solved_example,
                    "tofind": to_find,
                    "example": str(math_solving),
                    "type": operation_type,
                }
            )
        return context
