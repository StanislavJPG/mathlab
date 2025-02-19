from django.views.generic import TemplateView


class SolveTaskBaseView(TemplateView):
    template_name = "base.html"
