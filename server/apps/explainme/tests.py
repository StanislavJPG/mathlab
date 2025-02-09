import time

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestExplainMe(TestCase):
    def test_explainme(self):
        first_question = "Що таке графік функції?"
        second_question = "Що таке матриці?"
        third_question = "Що таке комбінаторика?"

        for question in (first_question, second_question, third_question):
            start = time.time()
            url = reverse("explainme") + "?topic={}".format(question)

            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_time = time.time() - start
        self.assertLess(response_time, 3.5)
