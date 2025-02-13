from django.http import HttpRequest as HttpRequestBase

from django_htmx.middleware import HtmxDetails

from server.apps.users.models import CustomUser


class AuthenticatedHttpRequest(HttpRequestBase):
    """
    See more:
    https://github.com/typeddjango/django-stubs?tab=readme-ov-file#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
    """

    htmx: HtmxDetails
    user: CustomUser
