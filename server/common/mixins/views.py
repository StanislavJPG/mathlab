from boringavatars import avatar
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView

from server.common.http import AuthenticatedHttpRequest
from server.common.third_party_apps.boringavatar import (
    BORINGAVATARS_DEFAULT_COLORS,
    BORINGAVATARS_DEFAULT_VARIANT,
    BORINGAVATARS_DEFAULT_SQUARE,
)


class CacheMixin:
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super().dispatch)(*args, **kwargs)


class AvatarDetailViewMixin(DetailView):
    avatar_unique_field = None  # this is unique identifier of instance to render avatar
    avatar_variant = None  # choices: {beam, marble, pixel, sunset, bauhaus, ring}
    avatar_square = False

    def _get_nested_attr(self, obj, attr, default=None):
        for part in attr.split('__'):
            obj = getattr(obj, part, default)
            if obj is default:
                return default
        return obj

    @property
    def _is_fk(self) -> bool:
        return '__' in self.avatar_unique_field

    def get_avatar_unique_field(self):
        self.object = self.get_object()
        if self.avatar_unique_field is None:
            raise NotImplementedError(f'You have to set `avatar_unique_field` by {self.model.__name__} model field.')

        if self._is_fk:
            return self._get_nested_attr(self.object, self.avatar_unique_field)

        if not hasattr(self.object, self.avatar_unique_field):
            raise NotImplementedError(
                f'Specified `avatar_unique_field` field does not exists in {self.model.__name__} model.'
            )

        return getattr(self.object, self.avatar_unique_field)

    def get(self, request, *args, **kwargs):
        """
        See: https://github.com/riquedev/django-initials-avatar/blob/2d297bd449b8d02785b6b079a968e9a7cf044784/django_initials_avatar/views.py#L59
        """
        name = self.get_avatar_unique_field()
        return HttpResponse(
            avatar(
                name=name,
                variant=self.avatar_variant if self.avatar_variant else BORINGAVATARS_DEFAULT_VARIANT,
                colors=BORINGAVATARS_DEFAULT_COLORS,
                square=self.avatar_square if self.avatar_square else BORINGAVATARS_DEFAULT_SQUARE,
            ),
            content_type='image/svg+xml',
        )


class HXViewMixin:
    pass_only_htmx_request = True  # pass request only if it's triggered by htmx

    def dispatch(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if self.pass_only_htmx_request and not self.request.htmx:
            return HttpResponse(status=405)
        return super().dispatch(request, *args, **kwargs)
