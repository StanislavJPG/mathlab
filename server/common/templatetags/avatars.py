from django.template.defaultfilters import register
from django.utils.safestring import mark_safe

from server.common.third_party_apps.boringavatar import BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST
from server.common.utils.defaults import get_default_user_pic


@register.simple_tag
@mark_safe
def get_instance_avatar(
    instance, size: int = None, is_square: bool = False, as_href: bool = False, href_url: str = None
):
    def link_wrapper(html):
        if as_href or href_url and instance:
            return f'<a href="{instance.get_absolute_url() if not href_url else href_url}" target="_blank">{html}</a>'
        return html

    if hasattr(instance, 'custom_avatar'):
        return link_wrapper(
            instance.html_tag_avatar(
                size=[size, size] if size else BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST,
                square=is_square,
            )
        )
    user_default_pic = get_default_user_pic(is_square=is_square)
    return link_wrapper(
        f'<img src="{user_default_pic}" width="{size}" height="{size}" '
        f'alt="avatar" class="{"rounded-circle" if not is_square else "squared rounded"}">'
    )
