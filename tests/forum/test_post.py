from random import choices

from django.urls import reverse

from server.apps.forum.logic.post_management import PostCreateView
from server.apps.forum.models import PostCategory
from tests.mixins import TheoristTest


class PostTest(TheoristTest):
    def setUp(self):
        super().setUp()
        PostCategory.create_data()

    def test_post_creation_view(self):
        self.client.force_login(self.user)
        request = self.factory.post(
            reverse('forum:hx-post-create'),
            data={
                'title': self.fake.sentence(nb_words=5),
                'content': self.fake.text(max_nb_chars=2000),
                'theorist': self.theorist,
                'categories': choices(PostCategory.objects.all(), k=3),
            },
        )
        response = self.get_response(cbv=PostCreateView, request=request)

        self.assertEqual(response.status_code, 200)

    def test_post_unauthorized_creation_view(self):
        request = self.factory.post(
            reverse('forum:hx-post-create'),
            data={
                'title': self.fake.sentence(nb_words=5),
                'content': self.fake.text(max_nb_chars=2000),
                'theorist': self.theorist,
                'categories': choices(PostCategory.objects.all(), k=3),
            },
        )
        response = self.get_response(cbv=PostCreateView, request=request, is_anonymous=True)

        self.assertEqual(response.status_code, 302)
