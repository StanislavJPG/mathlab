import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from forum.models import Post
from forum.views import PostSearchView
from users.models import CustomUser


class TestForum(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.new_user = CustomUser.objects.create(username='username', email='test@test.com', password='password')

        self.client.login(email='test@test.com', password='password')
        self.token = Token.objects.create(user=self.new_user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.new_post = Post.objects.create(title='test_title', content='test_content', user=self.new_user)

    def test_question_creation(self):
        url = reverse('forum-q-creation')
        data = {'title': 'TestTitle TestTitle',
                'category': [1, 4, 5],
                'content': 'TestContent TestContent'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_comment(self):
        url = reverse('forum-q', kwargs={'q_id': self.new_post.id,
                                         'title': self.new_post.title})
        data = {'comment': 'TestComment TestComment'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_post_rate(self):
        url = reverse('forum-q-rate', kwargs={'q_id': self.new_post.id,
                                              'title': self.new_post.title})
        data = {'like': 'like',
                'dislike': 'dislike'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_comment_rate(self):
        url = reverse('forum-q-comm-rate', kwargs={'q_id': self.new_post.id,
                                                   'title': self.new_post.title})

        data = {'like': 'like',
                'dislike': 'dislike',
                'comm_id': 1,
                'user_id': self.new_user.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_post_search(self):
        url = reverse('forum-b-search')
        data = {'page': 1,
                'search_pattern': 'test_title'}

        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertIsInstance(response.context['posts'][0], dict)

    def test_delete_post(self):
        url = reverse('forum-base')
        data = {'post_id': self.new_post.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
