from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django_tables2 import SingleTableView

from server.apps.drafts.models import TheoristDrafts
from server.apps.drafts.tables import DraftsTable
from server.common.mixins.views import HXViewMixin


class TheoristDraftsBaseTemplateView(TemplateView):
    template_name = 'base_drafts.html'


class AbstractTheoristDraftsListView(LoginRequiredMixin, HXViewMixin, ListView):
    model = TheoristDrafts
    context_object_name = 'drafts'
    slug_url_kwarg = 'uuid'
    slug_field = 'theorist__uuid'


class TheoristDraftsAlbumListView(AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_album_list.html'


class TheoristDraftsTableListView(SingleTableView, AbstractTheoristDraftsListView):
    template_name = 'partials/drafts_table.html'
    table_class = DraftsTable
