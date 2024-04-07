from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.deprecation import MiddlewareMixin


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


class TokenMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if request.user.is_authenticated:
            token = request.user.auth_token.key
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
