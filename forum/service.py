from users.models import CustomUser as User


def make_rate(user_id: int, score: int) -> None:
    user = User.objects.get(pk=user_id)
    user.score += score
    user.save()


def rank_creator_for_serializer(representation: dict) -> str:
    user_content = representation['score']

    if user_content < 50:
        user_content = 'Учень математики'

    elif 50 <= user_content < 100:
        user_content = 'Олімпіадник'

    elif 100 <= user_content < 200:
        user_content = 'Вчитель математики'

    elif 200 <= user_content < 600:
        user_content = 'Гуру математики'

    else:
        user_content = 'Володар математики'

    return user_content
