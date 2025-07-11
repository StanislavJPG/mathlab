from random import choices

import factory
from factory.base import T

from server.apps.forum.models import PostCategory
from server.apps.theorist.factories import TheoristFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Post'

    title = factory.Faker('sentence', nb_words=6)
    content = factory.Faker('text', max_nb_chars=2000)
    theorist = factory.SubFactory(TheoristFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        self.categories.add(*extracted)

    @classmethod
    def create(cls, **kwargs) -> T:
        PostCategory.create_data()
        kwargs['categories'] = choices(PostCategory.objects.all(), k=3)  # default behaviour
        return super().create(**kwargs)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.Comment'

    comment = factory.Faker('text', max_nb_chars=2000)

    post = factory.SubFactory(PostFactory)
    theorist = factory.SubFactory(TheoristFactory)


class CommentAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'forum.CommentAnswer'

    text_body = factory.Faker('text', max_nb_chars=400)

    comment = factory.SubFactory(CommentFactory)
    theorist = factory.SubFactory(TheoristFactory)
