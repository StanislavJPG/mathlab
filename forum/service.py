from users.models import CustomUser as User


def make_rate(request, user_id: int, score: int) -> None:
    user = User.objects.get(pk=user_id)

    if user.id != request.user.id:
        user.score += score
        user.save()
