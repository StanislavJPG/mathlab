import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.drafts.models import TheoristDrafts
import server.common.tables.attrs as table_attrs
from server.common.tables.mixins import CreatedAtTableMixin


class DraftsTable(CreatedAtTableMixin, tables.Table):
    label = tables.Column(verbose_name=_('Label'))
    draft = tables.Column(verbose_name=_('Draft'), attrs={'td': {'class': 'w-25'}})
    description = tables.Column(verbose_name=_('Description'), attrs={'td': {'class': 'w-25'}})
    created_at = tables.Column(verbose_name=_('Created at'), attrs={'td': {'class': 'w-25'}})
    actions = tables.TemplateColumn(
        template_name='partials/tables/drafts_actions.html',
        verbose_name=_('Actions'),
        attrs={'td': {'style': 'width: 5%; text-align: center; vertical-align: middle;'}},
    )

    class Meta:
        model = TheoristDrafts
        template_name = 'tables/bootstrap_htmx.html'
        fields = ('label', 'draft', 'description', 'created_at')
        attrs = {**table_attrs.get_default_table_attrs()}

    @mark_safe
    def render_draft(self, record, value):
        return f"""
        <a href="{record.get_draft_url()}"
           data-pswp-width="700"
           data-pswp-height="500"
           target="_blank">
          <img class="bd-placeholder-img" src="{record.get_draft_url()}">
        </a>
        """
