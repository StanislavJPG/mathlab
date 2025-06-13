from django.urls import reverse
from django.utils.crypto import get_random_string

from tests.testcases import TheoristTestCase


class TestTheorist(TheoristTestCase):
    ### Avatars

    def test_theorist_default_avatar_view(self):
        response = self.client.get(
            reverse('forum:theorist_profile:theorist-avatar', kwargs={'uuid': self.theorist.uuid})
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_avatar_upload_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_post(
            reverse('forum:theorist_profile:theorist-avatar-upload', kwargs={'uuid': self.theorist.uuid}),
            data={'custom_avatar': self.django_factory.ImageField()},
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_avatar_delete_view(self):
        self.client.force_login(self.user)
        self.theorist.custom_avatar = self.fake.image_url()
        self.theorist.save(update_fields=['custom_avatar'])
        avatar_before = self.theorist.custom_avatar
        response = self.client.hx_post(
            reverse('forum:theorist_profile:theorist-avatar-delete', kwargs={'uuid': self.theorist.uuid})
        )
        self.theorist.refresh_from_db()
        self.assertNotEquals(avatar_before, self.theorist.custom_avatar)
        self.assertEqual(response.status_code, 200)

    ### ///
    ### Profile

    def test_theorist_profile_detail_view(self):
        response = self.client.get(
            reverse(
                'forum:theorist_profile:base-page',
                kwargs={'pk': self.theorist.pk, 'full_name_slug': self.theorist.full_name_slug},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_profile_main_block_detail_view(self):
        response = self.client.hx_get(
            reverse(
                'forum:theorist_profile:hx-theorist-main-block',
                kwargs={'pk': self.theorist.pk, 'full_name_slug': self.theorist.full_name_slug},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_hx_theorist_profile_details_view(self):
        response = self.client.hx_get(
            reverse(
                'forum:theorist_profile:hx-theorist-details',
                kwargs={'pk': self.theorist.pk, 'full_name_slug': self.theorist.full_name_slug},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_last_activity_list_view(self):
        response = self.client.get(
            reverse('forum:theorist_profile:hx-theorist-last-activities', kwargs={'uuid': self.theorist.uuid})
        )
        self.assertEqual(response.status_code, 200)

    ### ///
    ### Profile settings

    def test_theorist_profile_settings_general_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:theorist_profile:settings:theorist-profile-settings'))
        self.assertEqual(response.status_code, 200)

    def test_theorist_profile_personal_info_form_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:settings:hx-profile-personal-info-form', kwargs={'uuid': self.theorist.uuid}
            ),
            data={'full_name': self.fake.user_name(), 'about_me': self.fake.text(max_nb_chars=150), 'country': 'AU'},
        )
        self.assertFormError(response.context['form'], 'country', [])
        self.assertFormError(response.context['form'], 'captcha', [])
        self.assertEqual(response.status_code, 200)

    def test_theorist_profile_email_configuration_form_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_post(reverse('forum:theorist_profile:settings:hx-profile-email-configurations-form'))
        self.assertEqual(response.status_code, 200)

    def test_theorist_profile_configurations_form_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:settings:hx-profile-configurations-form', kwargs={'uuid': self.theorist.uuid}
            )
        )
        for field in list(response.context['form'].fields):
            self.assertFormError(response.context['form'], field, [])
        self.assertEqual(response.status_code, 200)

    def test_theorist_profile_password_form_view(self):
        raw_password = 'new_password'
        self.user.set_password(raw_password)
        self.user.save()

        self.client.force_login(self.user)
        new_pass = get_random_string(length=40)
        response = self.client.hx_post(
            reverse('forum:theorist_profile:settings:hx-profile-password-form'),
            data={
                'oldpassword': raw_password,
                'password1': new_pass,
                'password2': new_pass,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_profile_deactivate_account_view(self):
        self.client.force_login(self.user)
        user_is_active_before = self.theorist.user.is_active
        response = self.client.post(
            reverse(
                'forum:theorist_profile:settings:hx-profile-deactivate-account-form',
                kwargs={'uuid': self.theorist.uuid},
            )
        )
        self.theorist.user.refresh_from_db()
        self.assertNotEquals(user_is_active_before, self.theorist.user.is_active)
        self.assertFalse(self.theorist.user.is_active)
        self.assertEqual(response.status_code, 200)

    ### ///
    ### Onboarding

    def _init_start_onboard_data(self):
        self.theorist.is_onboarded = False
        self.theorist.save(update_fields=['is_onboarded'])

    def test_onboarding_template_view(self):
        self.client.force_login(self.user)
        self._init_start_onboard_data()
        response = self.client.get(reverse('theorist_onboarding:base-page'))
        self.assertEqual(response.status_code, 200)

    def test_hx_onboard_form_view(self):
        self.client.force_login(self.user)
        self._init_start_onboard_data()
        response = self.client.hx_post(
            reverse('theorist_onboarding:hx-onboard-view', kwargs={'uuid': self.theorist.uuid}),
            data={'country': 'AU', 'about_me': self.fake.text(max_nb_chars=150)},
        )
        self.assertEqual(response.status_code, 200)

    ### ///
