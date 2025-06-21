import factory
from django.utils import timezone
from factory import fuzzy

from server.apps.theorist.factories import TheoristFactory


class TheoristChatRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'theorist_chat.TheoristChatRoom'

    first_member = factory.SubFactory(TheoristFactory)
    second_member = factory.SubFactory(TheoristFactory)

    last_sms_sent_at = fuzzy.FuzzyDateTime(timezone.now())


class TheoristMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'theorist_chat.TheoristMessage'

    message = factory.Faker('text', max_nb_chars=500)
    sender = factory.SubFactory(TheoristFactory)
    room = factory.SubFactory(TheoristChatRoomFactory)
