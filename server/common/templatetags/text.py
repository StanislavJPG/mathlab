from bs4 import BeautifulSoup
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe


@register.filter()
@mark_safe
def truncate_by_rows(text, truncate_by):
    lines = text.split('\n')
    truncated = '\n'.join(lines[: truncate_by + 1])

    soup = BeautifulSoup(truncated, 'html.parser')
    return soup.prettify()
