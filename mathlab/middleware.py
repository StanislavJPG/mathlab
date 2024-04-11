from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.contrib.auth import logout
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token


class AsyncMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        return response


class NoTokenFoundException(Exception):
    ...


class TokenMiddleware(MiddlewareMixin):
    """
        Token authorization middleware
    """
    @staticmethod
    def process_request(request):
        if request.user.is_authenticated:
            try:
                token = request.user.auth_token.key
                request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            except Token.DoesNotExist:
                """
                    NoTokenFoundException() will be raised if token does not exist == 500 error
                """
                logout(request)
                raise NoTokenFoundException()


class AccessControl(MiddlewareMixin):
    """
        Access Control to admin's manageable pages
    """
    @staticmethod
    def process_request(request):
        if "admin" in request.path_info or "auth" in request.path_info:
            if request.user.is_superuser:
                ...
            else:
                raise Http404()

