from django import template

register = template.Library()


@register.filter(name="page_convert")
def page_converter(stop, step):
    return [i // step + 1 for i in range(0, stop, step)]
