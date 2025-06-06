"""Utils for returning default data for keeping similarity in the whole project."""

import inspect

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


def get_default_colored_log(request, status_code) -> str:
    def format_path(cls):
        path = inspect.getfile(cls)
        full_view_path = '.'.join(path.split('/')[:-1])[1:] + '.'
        return full_view_path + cls.__name__

    try:
        view_class = request.resolver_match.func.view_class
        view_path = format_path(view_class)
    except AttributeError:
        view_path = 'VIEW'

    COLORS = {}
    COLORS.update(
        {
            'GET': '\033[92m',  # Green
            'POST': '\033[94m',  # Blue
            'PUT': '\033[93m',  # Yellow
            'DELETE': '\033[91m',  # Red
            'PATCH': '\033[95m',  # Magenta
        }
    )

    STATUS_COLORS = {
        200: '\033[92m',  # Green
        404: '\033[93m',  # Yellow
        500: '\033[91m',  # Red
    }

    method = request.method
    reset = '\033[0m'
    request_color = COLORS.get(method, reset)
    status_color = STATUS_COLORS.get(status_code, reset)

    default_logs_pattern = (
        f'{request_color}{request.method}{reset} | {view_path} - {request.path} - {status_color}{status_code}{reset}'
    )
    return default_logs_pattern
