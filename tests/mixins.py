from random import choice

from django.contrib.auth.models import AnonymousUser
from django_countries import Countries
from django_htmx.middleware import HtmxDetails

from django.test import TestCase, RequestFactory
from faker import Faker

from server.apps.theorist.models import Theorist
from server.apps.users.models import CustomUser


class TheoristTest(TestCase):
    fake = Faker()
    factory = RequestFactory(headers={'HX-Request': 'true'})

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username=self.fake.user_name(),
        )
        self.theorist = Theorist.objects.create(
            full_name=self.user.username, user=self.user, country=choice(list(Countries().countries))
        )
        self.theorist.apply_default_onboarding_data()
        self.theorist.save()

    def get_response(self, *, cbv, request, is_anonymous=False):
        self._extend_request_by_attrs(request)
        if is_anonymous:
            request.user = AnonymousUser()

        setattr(cbv, 'raise_exception', False)  # return only status codes, not Exceptions
        return cbv.as_view()(request)

    def _extend_request_by_attrs(self, request) -> None:
        request.user = self.user
        request.theorist = self.theorist
        request.htmx = HtmxDetails(request)  # because most of the views has HXViewMixin
