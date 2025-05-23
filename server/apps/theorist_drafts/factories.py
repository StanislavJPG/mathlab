from random import choice

import factory
from factory.base import T

from server.apps.theorist.factories import TheoristFactory


class TheoristDraftsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'theorist_drafts.TheoristDrafts'

    label = factory.Faker('paragraph', nb_sentences=1)
    description = factory.Faker('text', max_nb_chars=255)

    theorist = factory.SubFactory(TheoristFactory)

    @classmethod
    def create(cls, **kwargs) -> T:
        kwargs['draft'] = factory.django.ImageField(width=771, height=614, color=cls._random_color())
        return super().create(**kwargs)

    @classmethod
    def _random_color(cls):
        return choice(['red', 'green', 'blue', 'yellow', 'brown', 'orange'])
