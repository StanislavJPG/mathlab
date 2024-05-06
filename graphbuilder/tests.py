from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestGraphBuilder(TestCase):
    def test_graph(self):
        test_func = 'x**2'
        url = reverse('graphbuilder') + '?function={}'.format(test_func)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
