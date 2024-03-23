from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.decorators import async_only_middleware


@async_only_middleware
class AsyncMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        response = await self.get_response(request)
        return response
