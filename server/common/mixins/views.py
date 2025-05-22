import enum

from boringavatars import avatar
from braces.views import FormMessagesMixin
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from typing_extensions import assert_never

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

    @staticmethod
    def _get_nested_attr(obj, attr, default=None):
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
    """Use this view mixin with mixin `CaptchaForm` for your form class"""

    _is_captcha_processed = False

    def captcha_process(self, form):
        self._is_captcha_processed = True
        if not hasattr(form, 'HAS_CAPTCHA'):
            raise NotImplementedError('Use this view mixin with mixin `CaptchaForm` for your form class')
        form.clean_form_fail_attempts()
        form.captcha_success_try_session_push()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        form.captcha_session_push()
        return super().form_invalid(form)

    def form_valid(self, form):
        if not self._is_captcha_processed:
            raise NotImplementedError('You need to call `captcha_process(form)` inside your form_valid method.')
        return super().form_valid(form)


class RatedFormMessagesMixin(FormMessagesMixin):
    form_valid_message = ''  # default required attribute

    form_valid_like_message = None
    form_valid_dislike_message = None

    # attribute to check whether `get_form_valid_rated_messages` was called
    # use `set_default_behaviour` to make get_form_valid_message accessible
    _through_rate = False

    class DefaultConsts(enum.Enum):
        LIKE = 'like'
        DISLIKE = 'dislike'

    def get_form_valid_message(self):
        if self._through_rate is True:
            return super().get_form_valid_message()
        raise NotImplementedError(
            'You should use whether `get_form_valid_like_message` or `get_form_valid_dislike_message` methods'
        )

    def _pass_flag(self, _flag):
        rate_types = [item.value for item in self.DefaultConsts]
        if _flag not in rate_types:
            raise NotImplementedError(f'You should use next rate_types: {rate_types}')

    def get_form_valid_rated_messages(self, _flag: str):
        self._pass_flag(_flag)
        self._through_rate = True

        if _flag == self.DefaultConsts.LIKE.value:
            self.form_valid_message = self.form_valid_like_message
        elif _flag == self.DefaultConsts.DISLIKE.value:
            self.form_valid_message = self.form_valid_dislike_message
        else:
            assert_never(_flag)

        return self.get_form_valid_message()

    def get_form_valid_like_message(self):
        if not self.form_valid_like_message:
            raise NotImplementedError(
                'You need to specify `form_valid_like_message` attribute '
                'or override `get_form_valid_like_message` method.'
            )
        return self.get_form_valid_rated_messages(_flag=self.e.LIKE.value)

    def get_form_valid_dislike_message(self):
        if not self.form_valid_dislike_message:
            raise NotImplementedError(
                'You need to specify `form_valid_dislike_message` attribute '
                'or override `get_form_valid_dislike_message` method.'
            )
        return self.get_form_valid_rated_messages(_flag=self.e.DISLIKE.value)

    def set_default_messages_behaviour(self):
        self._through_rate = True

    @property
    def e(self):
        return self.DefaultConsts
