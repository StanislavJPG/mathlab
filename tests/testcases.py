import logging

import factory
from random import choice

from django.contrib.auth.models import AnonymousUser
from django.test.client import MULTIPART_CONTENT
from django_countries import Countries
from django_htmx.middleware import HtmxDetails

from django.test import TestCase, RequestFactory, Client
from faker import Faker

from server.apps.theorist.factories import TheoristFactory
from server.apps.theorist.models import Theorist
from server.apps.users.factories import CustomUserFactory
from server.apps.users.models import CustomUser


logger = logging.getLogger(__name__)


class HTMXClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {'HX-Request': 'true'}

    def hx_get(
        self,
        path,
        data=None,
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.get(
            path,
            data=data,
            follow=follow,
            secure=secure,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_post(
        self,
        path,
        data=None,
        content_type=MULTIPART_CONTENT,
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.post(
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_head(
        self,
        path,
        data=None,
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.head(
            path,
            data=data,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_options(
        self,
        path,
        data='',
        content_type='application/octet-stream',
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.options(
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_put(
        self,
        path,
        data='',
        content_type='application/octet-stream',
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.put(
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_patch(
        self,
        path,
        data='',
        content_type='application/octet-stream',
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.patch(
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_delete(
        self,
        path,
        data='',
        content_type='application/octet-stream',
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.delete(
            path,
            data=data,
            content_type=content_type,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )

    def hx_trace(
        self,
        path,
        data='',
        follow=False,
        secure=False,
        *,
        headers=None,
        query_params=None,
        **extra,
    ):
        if headers:
            self.headers.update(headers)
        return self.trace(
            path,
            data=data,
            secure=secure,
            follow=follow,
            headers=self.headers,
            query_params=query_params,
            **extra,
        )


class TheoristTestCase(TestCase):
    django_factory = factory.django
    fake = Faker()
    client_class = HTMXClient

    _hx_factory = RequestFactory(headers={'HX-Request': 'true'})
    _is_factory_used = False

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username=self.fake.user_name(),
        )
        self.theorist = Theorist.objects.create(
            full_name=self.user.username, user=self.user, country=choice(list(Countries().countries))
        )
        self.theorist.apply_default_onboarding_data()
        self.theorist.save()

    @property
    def hx_factory(self):
        self._is_factory_used = True
        return self._hx_factory

    @property
    def factory(self):
        self._is_factory_used = True
        return RequestFactory()

    @hx_factory.setter
    def hx_factory(self, val):
        if not isinstance(val, RequestFactory):
            raise ValueError('value must be RequestFactory instance')

        self._is_factory_used = True
        self._hx_factory = val

    def get_response(
        self,
        *,
        cbv,
        request,
        is_anonymous=False,  # for unauthorized testing purposes
        is_dummy_user=False,  # when we need to use other user than self.user
        is_dummy_theorist=False,  # when we need to use other theorist than self.theorist
        return_view_instance=False,
        kwargs=None,
    ):
        """
        Actually, not recommended to use this method.
        Use it only when we need to extend RequestFactory instance by custom attributes.
        """
        if not self._is_factory_used:
            raise ValueError('Use `self.factory` or `self.hx_factory` as request with `self.get_response()`.')

        self._extend_request_by_attrs(request, is_anonymous, is_dummy_user, is_dummy_theorist)

        setattr(cbv, 'raise_exception', False)  # return only status codes, not Exceptions
        view = cbv.as_view()

        view_instance = cbv()
        view_instance.request = request
        view_instance.kwargs = kwargs or {}

        view_to_return = view(request, **(kwargs or {}))

        logger.warning(
            f'{cbv.__name__} - \033[95m{view_to_return.status_code}\033[0m  '
            f'\033[93mWARNING: This test was processed by using `self.factory` or `self.hx_factory`. '
            f'If it is not necessary, use `self.client` without extra `self.response()` instead.\033[0m '
        )

        return view_instance if return_view_instance else view_to_return

    def _extend_request_by_attrs(
        self,
        request,
        is_anonymous=False,  # for unauthorized testing purposes
        is_dummy_user=False,  # when we need to use other user than self.user
        is_dummy_theorist=False,  # when we need to use other theorist than self.theorist
    ) -> None:
        request.user = self.user
        request.theorist = self.theorist
        request.htmx = HtmxDetails(request)  # because most of the views has HXViewMixin

        if is_anonymous and not is_dummy_user:
            request.user = AnonymousUser()

        if is_dummy_user:
            dummy_user = CustomUserFactory.create()
            request.user = dummy_user

        if is_dummy_theorist:
            dummy_theorist = TheoristFactory.create()
            request.theorist = dummy_theorist
