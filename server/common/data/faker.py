from server.apps.forum.factories import PostFactory, CommentFactory
from server.apps.theorist.factories import TheoristFactory
from server.apps.users.factories import CustomUserFactory


class BaseFakeDataGenerator(object):
    default_success_label = '%s %s was successfully generated.'

    @classmethod
    def _base_generator(cls, *, factory_class, iterations: int = 1, label='fake instances'):
        print('Generation of fake data...')
        for _ in range(iterations):
            factory_class.create()
        print('Generation of fake data is done!')
        return cls.default_success_label % (iterations, label)


class FakeDataGenerator(BaseFakeDataGenerator):
    """
    Basically, it's possible to generate fake data with own factory using `_base_generator()`
    But child class `FakeDataGenerator` provides convenient way to create fake data via
    already declared methods
    """

    @classmethod
    def generate_fake_users(cls, iterations: int = 1):
        return cls._base_generator(factory_class=CustomUserFactory, iterations=iterations, label='fake users')

    @classmethod
    def generate_fake_theorists(cls, iterations: int = 1):
        return cls._base_generator(factory_class=TheoristFactory, iterations=iterations, label='fake theorists')

    @classmethod
    def generate_fake_posts(cls, iterations: int = 1):
        return cls._base_generator(factory_class=PostFactory, iterations=iterations, label='fake posts')

    @classmethod
    def generate_fake_comments(cls, iterations: int = 1):
        return cls._base_generator(factory_class=CommentFactory, iterations=iterations, label='fake comments')
