"""Utils for returning default data for keeping similarity in the whole project."""

from django.conf import settings
from django.templatetags.static import static

from typing_extensions import assert_never

from django.utils.translation import gettext_lazy as _


def get_default_nonexistent_label(*, brisk=True, obj='') -> str:
    """
    function for nullable fields in models.
    Important goal of function is to keep consistency and similarity in project.
    """
    # TODO: In future need to make mapping by Model class and it's empty string value,
    #  if there is will be a non-brisk object that could have a nullable field
    if brisk:
        label = _('Unknown user')
    elif not brisk and obj:
        label = _(f'Unknown {obj}')
    else:
        assert_never(obj)
    return label


def get_default_user_pic(is_square):
    return static('img/base/user.png') if not is_square else static('img/base/squared_user.png')


def get_icon_for_contenttype_model(contenttype_obj, fail_silently=False):
    to_return = None
    try:
        for instance in settings.MODELS_TO_ICONS:
            if f'{contenttype_obj.app_label}.{contenttype_obj.model}' == instance[0].lower():
                to_return = instance[1]
    except AttributeError:
        if fail_silently:
            return None
        raise TypeError('contenttype_obj must be an instance of ContentType')

    if not to_return and not fail_silently:
        raise NotImplementedError('Model "{}" not found in `settings.MODELS_TO_ICONS`.'.format(contenttype_obj.model))
    return to_return
