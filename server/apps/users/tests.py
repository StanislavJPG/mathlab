from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestAccount(APITestCase):
    def setUp(self):
        # registration test

        url = reverse("register_view")
        data = {
            "email": "asdas12@asd",
            "username": "username",
            "password": "passwordPASSWORD",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_auth_user(self):
        url = reverse("login_view")
        data = {"email": "asdas12@asd", "password": "passwordPASSWORD"}

        response = self.client.post(url, data)

        token = Token.objects.get(user__username="username")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_logout_user(self):
        url = reverse("logout_view")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_password_reset(self):
        url = reverse("password_reset")
        response = self.client.post(url, data={"email": "asdas12@asd"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
