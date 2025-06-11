from django.test import TestCase
from django.urls import reverse


class TestCarousel(TestCase):
    def test_base_carousel_view(self):
        response = self.client.get(reverse('mathlab:carousel:hx-base-list'), headers={'HX-Request': 'true'})
        self.assertEqual(response.status_code, 200)

    def test_non_htmx_base_carousel_view(self):
        response = self.client.get(
            reverse('mathlab:carousel:hx-base-list'),
        )
        self.assertEqual(response.status_code, 403)
