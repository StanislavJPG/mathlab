from django.urls import reverse

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.apps.theorist.factories import TheoristFactory, TheoristFriendshipFactory
from tests.testcases import TheoristTestCase


class TestTheoristFriendship(TheoristTestCase):
    def setUp(self):
        super().setUp()
        self.dummy_theorist = TheoristFactory.create()
        self.friendship_request = TheoristFriendshipFactory.create(
            requester=self.dummy_theorist, receiver=self.theorist, status=TheoristFriendshipStatusChoices.PENDING.value
        )

    ### Theorist Blacklist

    def test_theorist_black_list_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(reverse('forum:theorist_profile:friendship:hx-theorist-community-blacklist'))
        self.assertEqual(response.status_code, 200)

    def test_theorist_unblock_from_blacklist_view(self):
        self.client.force_login(self.user)
        blacklist = self.theorist.blacklist
        blacklist.block(self.dummy_theorist)
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:friendship:theorist-blacklist-unblock',
                kwargs={'uuid': self.theorist.blacklist.uuid, 'theorist_uuid': self.dummy_theorist.uuid},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_block_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:friendship:theorist-blacklist-block',
                kwargs={'uuid': self.theorist.blacklist.uuid, 'theorist_uuid': self.dummy_theorist.uuid},
            )
        )
        self.assertEqual(response.status_code, 200)

    ### ///
    ### Friends

    def test_theorist_hx_friendship_template_view_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(
            reverse('forum:theorist_profile:friendship:hx-theorist-friendship', kwargs={'uuid': self.theorist.uuid})
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_friendship_list_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(
            reverse(
                'forum:theorist_profile:friendship:hx-theorist-friends-list',
                kwargs={'theorist_uuid': self.theorist.uuid, 'status': TheoristFriendshipStatusChoices.ACCEPTED},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_friendship_private_template_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('forum:theorist_profile:friendship:theorist-community-list'))
        self.assertEqual(response.status_code, 200)

    def test_theorist_private_community_list_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(
            reverse(
                'forum:theorist_profile:friendship:hx-theorist-community-list',
                kwargs={'status': TheoristFriendshipStatusChoices.ACCEPTED},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_hx_community_list_counter_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(
            reverse('forum:theorist_profile:friendship:hx-theorist-community-list-navs-counters')
        )
        self.assertEqual(response.status_code, 200)

    ### ///
    ### Friends management

    def test_theorist_friendship_create_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:friendship:theorist-friendship-request',
                kwargs={'theorist_uuid': self.dummy_theorist.uuid},
            )
        )
        self.assertEqual(response.status_code, 201)

    def test_theorist_friendship_accept_view(self):
        self.client.force_login(self.user)
        status_before = self.friendship_request.status
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:friendship:theorist-friendship-accept',
                kwargs={'uuid': self.friendship_request.uuid},
            )
        )
        self.friendship_request.refresh_from_db()
        self.assertNotEquals(status_before, self.friendship_request.status)
        self.assertEqual(TheoristFriendshipStatusChoices.ACCEPTED.value, self.friendship_request.status)
        self.assertEqual(response.status_code, 200)

    def test_theorist_friendship_reject_view(self):
        self.client.force_login(self.user)
        status_before = self.friendship_request.status
        response = self.client.hx_post(
            reverse(
                'forum:theorist_profile:friendship:theorist-friendship-reject',
                kwargs={'uuid': self.friendship_request.uuid},
            )
        )
        self.friendship_request.refresh_from_db()
        self.assertNotEquals(status_before, self.friendship_request.status)
        self.assertEqual(TheoristFriendshipStatusChoices.REJECTED.value, self.friendship_request.status)
        self.assertEqual(response.status_code, 200)

    def test_theorist_friendship_broke_up_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_delete(
            reverse(
                'forum:theorist_profile:friendship:theorist-friendship-broke-up',
                kwargs={'uuid': self.friendship_request.uuid},
            )
        )
        try:
            self.friendship_request.refresh_from_db()
        except self.friendship_request.DoesNotExist:
            self.assertEqual(response.status_code, 200)

    ### ///
