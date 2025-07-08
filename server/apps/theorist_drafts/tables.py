import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.theorist_drafts.models import TheoristDrafts
import server.common.tables.attrs as table_attrs
from server.common.tables.mixins import CreatedAtTableMixin


class CustomCheckBoxColumn(tables.CheckBoxColumn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = kwargs.get('attrs', {})
        attrs.update(
            {
                'th': {'class': 'text-center', 'hx-disable': ''},
                'td': {'class': 'text-center'},
            }
        )

    @property
    def header(self):
        return mark_safe(
            '<input type="checkbox" '
            '_="on click for checkbox in .checker set checkbox.checked to me.checked"'
            'id="general-checker"'
            'name="general-check" '
            'class="form-check-input general-checker"/>'
        )


class DraftsTable(CreatedAtTableMixin, tables.Table):
    check = CustomCheckBoxColumn(
        accessor='uuid',
        attrs={
            'input': {
                'class': 'form-check-input table-checker checker',
                'name': 'draftToShare',
            },
        },
    )
    label = tables.Column(verbose_name=_('Label'))
    draft = tables.Column(verbose_name=_('Draft'), attrs={'td': {'class': 'w-25'}})
    description = tables.Column(verbose_name=_('Description'), attrs={'td': {'class': 'w-25'}})
    created_at = tables.Column(verbose_name=_('Created at'), attrs={'td': {'class': 'w-25'}})
    actions = tables.TemplateColumn(
        template_name='partials/tables/drafts_actions.html',
        orderable=False,
        verbose_name=_('Actions'),
        attrs={'td': {'style': 'width: 5%; text-align: center; vertical-align: middle;'}},
    )

    def __init__(self, *args, **kwargs):
        self.theorist_from_url = kwargs.pop('theorist_from_url')
        super().__init__(*args, **kwargs)

    class Meta:
        model = TheoristDrafts
        template_name = 'tables/bootstrap_htmx.html'
        fields = ('check', 'label', 'draft', 'description', 'created_at')
        attrs = {**table_attrs.get_default_table_attrs()}

    def before_render(self, request):
        if request.theorist != self.theorist_from_url:
            self.columns.hide('actions')

    @mark_safe
    def render_draft(self, record, value):
        draft = record.get_draft()
        return f"""
        <a href="{draft.url}"
           data-pswp-width="{draft.width}"
           data-pswp-height="{draft.height}"
           target="_blank">
          <img class="bd-placeholder-img" style="max-width: 230px; max-height: 180px;" src="{draft.url}">
        </a>
        """
