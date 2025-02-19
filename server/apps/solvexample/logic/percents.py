from django.views.generic import TemplateView

from server.apps.solvexample.service import MathOperations


class PercentsTemplateView(TemplateView):
    template_name = "partials/percents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        example = self.request.GET.get("example")
        number = self.request.GET.get("num")
        percent = self.request.GET.get("percent")
        operation_type: str = self.request.GET.get("type")

        if operation_type:
            solved_example = MathOperations(
                example=[example, percent],
                to_find=number,
                operation_type=operation_type,
            ).solve_percent()

            context.update(
                {
                    "example": example,
                    "number": number,
                    "percent": percent,
                    "solved_example": solved_example,
                    "operation_type": operation_type,
                }
            )
        return context
