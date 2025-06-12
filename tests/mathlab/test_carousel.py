from django.test import TestCase
from django.urls import reverse

from tests.testcases import HTMXClient


class TestCarousel(TestCase):
    client_class = HTMXClient

    def test_base_carousel_view(self):
        response = self.client.hx_get(reverse('mathlab:carousel:hx-base-list'))
        self.assertEqual(response.status_code, 200)

    def test_non_htmx_base_carousel_view(self):
        response = self.client.get(
            reverse('mathlab:carousel:hx-base-list'),
        )
        self.assertEqual(response.status_code, 403)
