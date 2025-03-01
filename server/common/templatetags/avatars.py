from django.template.defaultfilters import register
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from server.common.third_party_apps.boringavatar import BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST


@register.simple_tag
@mark_safe
def get_instance_avatar(instance, size: int = None, square: bool = False):
    if hasattr(instance, 'custom_avatar'):
        return instance.html_tag_avatar(
            size=[size, size] if size else BORINGAVATARS_DEFAULT_SIZE_QUALITY_LIST,
            square=square,
        )
    return (
        f'<img src="{static("img/base/user.png")}" width="{size}" height="{size}" '
        f'alt="avatar" class="{"rounded-circle" if not square else "squared"}">'
    )
