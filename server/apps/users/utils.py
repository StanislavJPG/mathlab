from allauth.utils import build_absolute_uri
from django.db import transaction
from django.http import HttpResponseForbidden, HttpRequest
from django.urls import reverse

from server.apps.users.models import CustomUser as User


@transaction.atomic
def make_rate(request, user: int | User, score: int) -> None:
    try:
        user = User.objects.get(pk=user) if isinstance(user, int) else user

        if user.id != request.user.id:
            user.score += score
            user.save()
    except Exception:
        raise HttpResponseForbidden
    finally:
        user.update_rank()


def get_email_verification_url(request: HttpRequest, emailconfirmation) -> str:
    url = reverse('users:account-confirm-email-view', args=[emailconfirmation.key])
    url = build_absolute_uri(request, url)
    return url
