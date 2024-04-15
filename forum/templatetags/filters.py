from django import template
from translate import Translator

register = template.Library()


# @register.filter(name='translate')
# def translate(value):
#     translator = Translator(to_lang='uk')
#     translation = translator.translate(value)
#     return translation


@register.filter
def page_converter(stop, step):
    return [i // step + 1 for i in range(0, stop, step)]


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def url_hyphens_replace(value: str):
    value = value.replace(' ', '-')
    value = value.replace('?', '-')
    return value


# register.filter("translate", translate)
register.filter("index", index)
register.filter('hyphens_add', url_hyphens_replace)
register.filter('page_convert', page_converter)
