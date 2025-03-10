import json

from django.contrib.messages import get_messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from server.apps.theorist.models import Theorist
from server.common.utils.urls import is_excluded_path


class HTMXToastMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        messages = [{'message': message.message, 'tags': message.tags} for message in get_messages(request)]

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


class OnboardingMiddleware(MiddlewareMixin):
    """Theorist will always be redirected to the onboarding page if he is not onboarded yet."""

    def process_request(self, request):
        if (
            request.user.is_authenticated
            and not request.user.is_superuser
            and not request.theorist.is_onboarded
            and not is_excluded_path(request)
        ):
            return redirect(reverse('theorist_onboarding:base-page'))
