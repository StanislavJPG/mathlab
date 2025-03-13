from django.template.defaultfilters import register
from django.urls import reverse


@register.simple_tag(takes_context=True)
def absolute_url(context, view_name, *args, **kwargs):
    request = context['request']
    return request.build_absolute_uri(reverse(view_name, args=args, kwargs=kwargs))


@register.simple_tag(takes_context=True)
def classes_by_lookup_url(context, instance, url_lookup_kwarg):
    """
    Use this simple_tag inside class=""
    Example = class="row {% classes_by_lookup_url comment 'comment' %}"
    """
    request = context['request']
    return 'bg-warning-subtle rounded fadeDiv' if request.GET.get(url_lookup_kwarg) == str(instance.uuid) else ''
