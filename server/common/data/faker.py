from server.apps.forum.factories import PostFactory, CommentFactory
from server.apps.theorist.factories import TheoristFactory
from server.apps.users.factories import CustomUserFactory


class FakeDataGenerator(object):
    default_success_label = '%s %s was successfully generated.'

    @classmethod
    def generate_fake_users(cls, repeats: int = 1):
        print('Generation of fake data...')
        for _ in range(repeats):
            CustomUserFactory.create()
        print('Generation of fake data is done!')
        return cls.default_success_label % (repeats, 'fake users')

    @classmethod
    def generate_fake_theorists(cls, repeats: int = 1):
        print('Generation of fake data...')
        for _ in range(repeats):
            TheoristFactory.create()
        print('Generation of fake data is done!')
        return cls.default_success_label % (repeats, 'fake theorists')

    @classmethod
    def generate_fake_posts(cls, repeats: int = 1):
        print('Generation of fake data...')
        for _ in range(repeats):
            PostFactory.create()
        print('Generation of fake data is done!')
        return cls.default_success_label % (repeats, 'fake posts')

    @classmethod
    def generate_fake_comments(cls, repeats: int = 1):
        print('Generation of fake data...')
        for _ in range(repeats):
            CommentFactory.create()
        print('Generation of fake data is done!')
        return cls.default_success_label % (repeats, 'fake comments')
