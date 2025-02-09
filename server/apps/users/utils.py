from django.db import transaction
from django.http import HttpResponseForbidden

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
