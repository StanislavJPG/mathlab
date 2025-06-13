from allauth.account.forms import default_token_generator
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from faker import Faker

from server.apps.users.factories import CustomUserFactory


class TestCustomUser(TestCase):
    fake = Faker()

    def setUp(self):
        self.user = CustomUserFactory.create()
        self.theorist = self.user.create_initial_theorist()
        self.theorist.apply_default_onboarding_data()
        self.theorist.save()

    def test_custom_base_auth_view(self):
        response = self.client.get(reverse('users:base-auth'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        new_pass = get_random_string(length=40)
        self.user.set_password(new_pass)
        self.user.save()
        response = self.client.post(reverse('users:login-view'), data={'login': self.user.email, 'password': new_pass})
        user_from_request_session = get_user(self.client)
        self.assertEqual(self.user, user_from_request_session)
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self):
        new_pass = get_random_string(length=40)
        email = self.fake.email()
        response = self.client.post(
            reverse('users:register-view'),
            data={'email': email, 'username': self.fake.user_name(), 'password1': new_pass, 'password2': new_pass},
        )
        user_from_request_session = get_user(self.client)
        self.assertEqual(email, user_from_request_session.email)
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.force_login(self.user)
        user_before_logout = get_user(self.client)
        response = self.client.post(reverse('users:logout-view'), follow=True)
        self.assertFalse(isinstance(user_before_logout, AnonymousUser))
        self.assertTrue(isinstance(get_user(self.client), AnonymousUser))
        self.assertEqual(response.status_code, 200)

    def test_confirm_email_view(self):
        self.client.force_login(self.user)
        email = EmailAddress.objects.create(user=self.user, email=self.user.email)
        key = EmailConfirmationHMAC(email).key
        response = self.client.post(reverse('users:account-confirm-email-view', args=[key]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_view(self):
        response = self.client.post(
            reverse('users:reset-password-view'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_from_key_view(self):
        new_pass = get_random_string(length=40)
        temp_key = default_token_generator.make_token(self.user)
        uid = user_pk_to_url_str(self.user)
        response = self.client.post(
            reverse('users:reset-password-key-view', kwargs={'uidb36': uid, 'key': temp_key}),
            data={'password1': new_pass, 'password2': new_pass},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
