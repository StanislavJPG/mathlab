from django.contrib.auth.mixins import AccessMixin
from django.views.generic import TemplateView

from server.apps.theorist.models import Theorist


class TheoristDraftsBaseTemplateView(AccessMixin, TemplateView):
    template_name = 'base_drafts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theorist'] = Theorist.objects.filter(full_name_slug=self.kwargs['full_name_slug']).first()
        return context
