from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django_tables2 import SingleTableView
from render_block import render_block_to_string

from server.apps.drafts.models import TheoristDrafts, TheoristDraftsConfiguration
from server.apps.drafts.tables import DraftsTable
from server.common.http import AuthenticatedHttpRequest
from server.common.mixins.views import HXViewMixin


class TheoristDraftsBaseTemplateView(TemplateView):
    template_name = 'base_drafts.html'

    def get_context_data(self, **kwargs):
        self.request: AuthenticatedHttpRequest
        context = super().get_context_data(**kwargs)
        context['theorist'] = self.request.theorist
        context['configuration'] = self.request.theorist.drafts_configuration
        return context


class AbstractTheoristDraftsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristDrafts
    context_object_name = 'drafts'

    def get_queryset(self):
        return super().get_queryset().filter(theorist__drafts_configuration__uuid=self.kwargs['uuid'])


class TheoristDraftsAlbumListView(AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_album_list.html'


class TheoristDraftsTableListView(SingleTableView, AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_table.html'
    table_class = DraftsTable


class HXTheoristDraftsSearchView(LoginRequiredMixin, HXViewMixin, View):
    template_name = 'base_drafts.html'

    def get(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        search_draft = self.request.GET.get('search_draft')
        if search_draft:
            try:
                configuration = TheoristDraftsConfiguration.objects.filter(
                    Q(uuid=self.request.GET.get('search_draft'))
                    & (Q(is_public_available=True) | Q(theorist=self.request.theorist))
                ).first()
            except ValidationError:
                configuration = ''
        else:
            configuration = TheoristDraftsConfiguration.objects.get(theorist=self.request.theorist)

        context = {
            'theorist': getattr(configuration, 'theorist', ''),
            'configuration': configuration,
            'view': self.request.GET.get('view'),
        }
        rendered_block = render_block_to_string(self.template_name, 'drafts', context, self.request)
        return HttpResponse(content=rendered_block)
