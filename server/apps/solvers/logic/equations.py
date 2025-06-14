from django.views.generic import TemplateView


class EquationsTemplateView(TemplateView):
    """Maybe in the future, will make this functionality only for auth users or only for paid."""

    template_name = 'partials/equations.html'
