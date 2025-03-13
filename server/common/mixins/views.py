from boringavatars import avatar
from django.contrib.auth.mixins import AccessMixin
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
    avatar_variant = BORINGAVATARS_DEFAULT_VARIANT  # choices: {beam, marble, pixel, sunset, bauhaus, ring}
    avatar_square = BORINGAVATARS_DEFAULT_SQUARE

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
                variant=self.avatar_variant,
                colors=BORINGAVATARS_DEFAULT_COLORS,
                square=self.avatar_square,
            ),
            content_type='image/svg+xml',
        )


class HXViewMixin(AccessMixin):
    pass_only_htmx_request = True  # pass request only if it's triggered by htmx
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.request: AuthenticatedHttpRequest
        if self.pass_only_htmx_request and not self.request.htmx:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CaptchaViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        form.captcha_session_push()
        return super().form_invalid(form)

    def form_valid(self, form):
        form.clean_form_fail_attempts()
        return super().form_valid(form)


class InstanceURLMixin:
    """
    We need to pass additional page kwarg name to prevent kwargs conflicts.
    Example:
        We copy link from base page. We put this URL in searchbar.
        What would be if kwargs name was `page`:
            We went to instance what we searched by URL. But main pagination is not work (1, 2, 3).
            Because it gets settled `page` kwarg from the base page. ?page=3?uuid=...
            And it will try to get exact this `page` number from the searchbar, but not from pagination in HTML.
    """

    page_custom_kwarg = None

    def get_page_custom_kwarg(self):
        if not self.page_custom_kwarg:
            raise NotImplementedError('You must to specify `page_custom_kwarg`.')

        return self.page_custom_kwarg

    @property
    def page_kwarg(self):
        page_custom_kwarg = self.get_page_custom_kwarg()
        page_kwarg = (
            page_custom_kwarg
            if (self.request.GET.get(page_custom_kwarg) and not self.request.GET.get('page'))
            else 'page'
        )
        return page_kwarg

    # @property
    # def _get_classes_by_lookup_url(self):
    #     return 'bg-warning-subtle rounded' if self.request.GET.comment == comment.uuid"
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['get_classes_by_lookup_url'] = self
    #     return context
