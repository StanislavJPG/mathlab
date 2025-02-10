from django import template

register = template.Library()


@register.filter(name="hyphens_add")
def url_hyphens_replace(value: str):
    value = value.replace(" ", "-")
    value = value.replace("?", "-")
    return value.lower()
