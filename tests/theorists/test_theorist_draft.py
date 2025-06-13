import base64
import uuid
from io import BytesIO

from PIL import Image
from django.urls import reverse

from server.apps.theorist_drafts.factories import TheoristDraftsFactory
from server.apps.theorist_drafts.logic.drafts import TheoristDraftsAlbumListView
from server.apps.theorist_drafts.models import TheoristDrafts
from tests.testcases import TheoristTestCase


def _generate_base64_image():
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{base64_img}'


class TestTheoristDraft(TheoristTestCase):
    def setUp(self):
        super().setUp()
        self.theorist_draft = TheoristDraftsFactory.create(theorist=self.theorist)

    def test_theorist_drafts_base_template_view(self):
        response = self.client.get(reverse('mathlab:drafts:base-drafts'))
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_album_list_view(self):
        self.client.force_login(self.user)
        drafts_configuration = self.theorist.drafts_configuration
        response = self.client.hx_get(
            reverse('mathlab:drafts:drafts-album-list', kwargs={'drafts_configuration_uuid': drafts_configuration.uuid})
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_album_list_with_search_view(self):
        drafts_configuration = self.theorist.drafts_configuration
        request = self.hx_factory.get(
            reverse('mathlab:drafts:drafts-album-list', kwargs={'drafts_configuration_uuid': drafts_configuration.uuid})
            + f'?search_draft={uuid.uuid4()}'
        )
        response = self.get_response(
            cbv=TheoristDraftsAlbumListView,
            request=request,
            kwargs={'drafts_configuration_uuid': drafts_configuration.uuid},
            is_dummy_user=True,
            is_dummy_theorist=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_table_list_view(self):
        self.client.force_login(self.user)
        drafts_configuration = self.theorist.drafts_configuration
        response = self.client.hx_get(
            reverse('mathlab:drafts:drafts-table-list', kwargs={'drafts_configuration_uuid': drafts_configuration.uuid})
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_table_list_with_search_view(self):
        drafts_configuration = self.theorist.drafts_configuration
        request = self.hx_factory.get(
            reverse('mathlab:drafts:drafts-table-list', kwargs={'drafts_configuration_uuid': drafts_configuration.uuid})
            + f'?search_draft={uuid.uuid4()}'
        )
        response = self.get_response(
            cbv=TheoristDraftsAlbumListView,
            request=request,
            kwargs={'drafts_configuration_uuid': drafts_configuration.uuid},
            is_dummy_user=True,
            is_dummy_theorist=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_search_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_get(reverse('mathlab:drafts:drafts-search') + '?search_draft={}'.format(uuid.uuid4()))
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_create_view(self):
        self.client.force_login(self.user)
        label = 'Unique test label'
        response = self.client.hx_post(
            reverse('mathlab:drafts:drafts-create'), data={'label': label, 'draft': _generate_base64_image()}
        )
        self.assertTrue(TheoristDrafts.objects.filter(label=label).exists())
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_update_view(self):
        self.client.force_login(self.user)
        old_draft_label = self.theorist_draft.label
        label_to_set = 'Updated unique test label'
        response = self.client.hx_post(
            reverse('mathlab:drafts:drafts-edit', kwargs={'uuid': self.theorist_draft.uuid}),
            data={
                'label': label_to_set,
            },
        )
        self.theorist_draft.refresh_from_db()
        self.assertNotEquals(old_draft_label, self.theorist_draft.label)
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_upload_view(self):
        self.client.force_login(self.user)
        label = 'Unique test label'
        draft_test_instance = TheoristDraftsFactory.create()
        response = self.client.hx_post(
            reverse('mathlab:drafts:drafts-upload'), data={'label': label, 'draft': draft_test_instance.draft}
        )
        self.assertTrue(TheoristDrafts.objects.filter(label=label).exists())
        self.assertEqual(response.status_code, 200)

    def test_theorist_drafts_delete_view(self):
        self.client.force_login(self.user)
        response = self.client.hx_delete(
            reverse('mathlab:drafts:drafts-delete', kwargs={'uuid': self.theorist_draft.uuid}),
        )
        self.assertEqual(response.status_code, 200)
