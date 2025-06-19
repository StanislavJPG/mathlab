from bs4 import BeautifulSoup
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from server.common.utils.defaults import get_icon_for_contenttype_model


@register.filter()
@mark_safe
def truncate_by_rows(text, truncate_by):
    lines = text.split('\n')
    truncated = '\n'.join(lines[: truncate_by + 1])

    soup = BeautifulSoup(truncated, 'html.parser')
    return soup.prettify()


@register.simple_tag
@mark_safe
def icon_for_contenttype_model(contenttype, style='', add_class=''):
    icon_class = get_icon_for_contenttype_model(contenttype, fail_silently=True)
    return '<i class="{add_class} {icon_class}" style="{style}"></i>'.format(
        add_class=add_class, style=style, icon_class=icon_class
    )
