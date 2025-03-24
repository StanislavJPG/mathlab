import django_tables2 as tables
from django.utils.safestring import mark_safe

from server.apps.drafts.models import TheoristDrafts
import server.common.tables.attrs as table_attrs


class DraftsTable(tables.Table):
    draft = tables.Column(attrs={'td': {'style': 'width: 25%'}})

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
