import json

from django.contrib.messages import get_messages
from django.utils.deprecation import MiddlewareMixin


class HTMXToastMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        messages = [
            {"message": message.message, "tags": message.tags}
            for message in get_messages(request)
        ]

        if messages:
            existing_trigger = response.headers.get("HX-Trigger", "{}")
            existing_data = json.loads(existing_trigger)

            existing_data.setdefault("messages", []).extend(messages)

            response.headers["HX-Trigger"] = json.dumps(existing_data)

        return response
