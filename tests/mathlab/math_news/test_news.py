from django.test import TestCase
from django.urls import reverse


class TestNews(TestCase):
    def test_news_base_template_view(self):
        response = self.client.get(reverse('mathlab:math_news:base-math-news'))
        self.assertEqual(response.status_code, 200)

    def test_hx_news_list_view(self):
        response = self.client.get(reverse('mathlab:math_news:hx-math-news-list'), headers={'HX-Request': 'true'})
        self.assertEqual(response.status_code, 200)

    def test_non_htmx_hx_news_list_view(self):
        response = self.client.get(reverse('mathlab:math_news:hx-math-news-list'))
        self.assertEqual(response.status_code, 403)
