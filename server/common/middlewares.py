import json

from django.contrib.messages import get_messages
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from server.apps.theorist.models import Theorist


class HTMXToastMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        messages = [
            {'message': message.message, 'tags': message.tags}
            for message in get_messages(request)
        ]

        if messages:
            existing_trigger = response.headers.get('HX-Trigger', '{}')
            existing_data = json.loads(existing_trigger)

            existing_data.setdefault('messages', []).extend(messages)

            response.headers['HX-Trigger'] = json.dumps(existing_data)

        return response


class UnifiedRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr('request', 'theorist'):
            request.theorist = SimpleLazyObject(lambda: self.get_theorist(request))

    def get_theorist(self, request):
        if request.user.is_authenticated:
            return Theorist.objects.filter(user=request.user).first()
        return None
