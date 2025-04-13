from django.template.defaultfilters import register
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from server.common.third_party_apps.boringavatar import BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST


@register.simple_tag
@mark_safe
def get_instance_avatar(
    instance, size: int = None, is_square: bool = False, as_href: bool = False, href_url: str = None
):
    def link_wrapper(html):
        wrapped_avatar_html = (
            f'<a href="{instance.get_absolute_url() if not href_url else href_url}" target="_blank">{html}</a>'
        )
        return wrapped_avatar_html if as_href or href_url else html

    if hasattr(instance, 'custom_avatar'):
        return link_wrapper(
            instance.html_tag_avatar(
                size=[size, size] if size else BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST,
                square=is_square,
            )
        )
    return link_wrapper(
        f'<img src="{static("img/base/user.png")}" width="{size}" height="{size}" '
        f'alt="avatar" class="{"rounded-circle" if not is_square else "squared"}">'
    )
