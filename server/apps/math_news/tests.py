from django.test import TestCase
from rest_framework import status

from server.apps.math_news.tasks import let_find_news


class TestNewsTask(TestCase):
    def test_let_find_news(self):
        response = let_find_news()
        self.assertIn(response, (status.HTTP_201_CREATED, status.HTTP_409_CONFLICT))
