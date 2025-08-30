from server.apps.forum.factories import PostFactory, CommentFactory, CommentAnswerFactory
from server.apps.game_area.factories import MathQuizFactory, MathExpressionFactory
from server.apps.theorist.factories import TheoristFactory, TheoristFriendshipFactory
from server.apps.theorist_chat.factories import TheoristChatRoomFactory, TheoristMessageFactory
from server.apps.theorist_drafts.factories import TheoristDraftsFactory
from server.apps.users.factories import CustomUserFactory


class BaseFakeDataGenerator(object):
    default_success_label = '%s %s was successfully generated.'

    @classmethod
    def _base_generator(cls, *, factory_class, iterations: int = 1, label='instances', **kwargs):
        print(f'Generation of fake {label}...')
        for _ in range(iterations):
            factory_class.create(**kwargs)
        print(f'Generation of fake {label} is done!')

        return cls.default_success_label % (iterations, f'fake {label}')


class FakeDataGenerator(BaseFakeDataGenerator):
    """
    Basically, it's possible to generate fake data with own factory using `_base_generator()`
    But child class `FakeDataGenerator` provides convenient way to create fake data via
    already declared methods
    """

    @classmethod
    def generate_all(cls, each_iterations: int = 50):
        """This method prepares environment as production-alike by generation and creation fake data."""
        for _ in dir(cls):
            attr = getattr(cls, _)
            if callable(attr) and not _.startswith('_') and _ != 'generate_all':
                attr(iterations=each_iterations)
        return cls.default_success_label % (each_iterations, 'fake data of each instance')

    @classmethod
    def generate_fake_users(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(factory_class=CustomUserFactory, iterations=iterations, label='users', **kwargs)

    @classmethod
    def generate_fake_theorists(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(factory_class=TheoristFactory, iterations=iterations, label='theorists', **kwargs)

    @classmethod
    def generate_fake_posts(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(factory_class=PostFactory, iterations=iterations, label='posts', **kwargs)

    @classmethod
    def generate_fake_comments(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(factory_class=CommentFactory, iterations=iterations, label='comments', **kwargs)

    @classmethod
    def generate_fake_comment_answers(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(
            factory_class=CommentAnswerFactory, iterations=iterations, label='comment answers', **kwargs
        )

    @classmethod
    def generate_fake_chat_rooms(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(
            factory_class=TheoristChatRoomFactory, iterations=iterations, label='chat rooms', **kwargs
        )

    @classmethod
    def generate_fake_chat_messages(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(
            factory_class=TheoristMessageFactory, iterations=iterations, label='chat messages', **kwargs
        )

    @classmethod
    def generate_fake_theorist_friendships(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(
            factory_class=TheoristFriendshipFactory, iterations=iterations, label='friendships', **kwargs
        )

    @classmethod
    def generate_fake_theorist_drafts(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(factory_class=TheoristDraftsFactory, iterations=iterations, label='drafts', **kwargs)

    @classmethod
    def generate_fake_math_quizzes(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(factory_class=MathQuizFactory, iterations=iterations, label='quizzes', **kwargs)

    @classmethod
    def generate_fake_math_expressions(cls, iterations: int = 1, **kwargs):
        return cls._base_generator(
            factory_class=MathExpressionFactory, iterations=iterations, label='expressions', **kwargs
        )


fake = FakeDataGenerator
