from random import choice

from django.contrib.auth.models import AnonymousUser
from django_countries import Countries
from django_htmx.middleware import HtmxDetails

from django.test import TestCase, RequestFactory
from faker import Faker

from server.apps.theorist.factories import TheoristFactory
from server.apps.theorist.models import Theorist
from server.apps.users.factories import CustomUserFactory
from server.apps.users.models import CustomUser


class TheoristTestCase(TestCase):
    fake = Faker()
    factory = RequestFactory()
    hx_factory = RequestFactory(headers={'HX-Request': 'true'})

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username=self.fake.user_name(),
        )
        self.theorist = Theorist.objects.create(
            full_name=self.user.username, user=self.user, country=choice(list(Countries().countries))
        )
        self.theorist.apply_default_onboarding_data()
        self.theorist.save()

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
        self._extend_request_by_attrs(request)
        if is_anonymous and not is_dummy_user:
            request.user = AnonymousUser()

        if is_dummy_user:
            dummy_user = CustomUserFactory.create()
            request.user = dummy_user

        if is_dummy_theorist:
            dummy_theorist = TheoristFactory.create()
            request.theorist = dummy_theorist

        setattr(cbv, 'raise_exception', False)  # return only status codes, not Exceptions
        view = cbv.as_view()

        view_instance = cbv()
        view_instance.request = request
        view_instance.kwargs = kwargs or {}

        return view_instance if return_view_instance else view(request, **(kwargs or {}))

    def _extend_request_by_attrs(self, request) -> None:
        request.user = self.user
        request.theorist = self.theorist
        request.htmx = HtmxDetails(request)  # because most of the views has HXViewMixin
