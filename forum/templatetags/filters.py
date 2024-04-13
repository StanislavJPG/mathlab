from django import template
from translate import Translator

register = template.Library()


@register.filter(name='translate')
def translate(value):
    translator = Translator(to_lang='uk')
    translation = translator.translate(value)
    return translation


@register.filter
def index(indexable, i):
    return indexable[i]


register.filter("translate", translate)
register.filter("index", index)
