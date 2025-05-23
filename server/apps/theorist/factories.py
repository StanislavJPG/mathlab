import factory
from django.utils import timezone
from django_countries import Countries
from factory import fuzzy

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.users.factories import CustomUserFactory


class TheoristFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'theorist.Theorist'

    user = factory.SubFactory(CustomUserFactory)

    full_name = factory.Faker('name')
    country = fuzzy.FuzzyChoice(choices=list(Countries().countries))
    about_me = factory.Faker('text', max_nb_chars=100)

    is_onboarded = True
    onboarding_date = fuzzy.FuzzyDateTime(timezone.now())

    social_media_url = factory.Faker('uri')
    website_url = factory.Faker('uri')


class TheoristFriendshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'theorist.TheoristFriendship'

    requester = factory.SubFactory(TheoristFactory)
    receiver = factory.SubFactory(TheoristFactory)

    status = factory.fuzzy.FuzzyChoice(choices=TheoristFriendshipStatusChoices.choices, getter=lambda x: x[0])
