from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from server.apps.complaints.factories import ComplaintFactory
from server.apps.complaints.logic.complaint_management import ComplaintCreateView
from server.apps.theorist.models import TheoristFriendship
from server.common.data.faker import fake
from tests.testcases import TheoristTestCase


class ComplaintsTest(TheoristTestCase):
    def setUp(self):
        super().setUp()
        fake.generate_all(each_iterations=1)
        accessed_models_map = ComplaintCreateView._map_of_accessed_models()
        self.labels = accessed_models_map.keys()
        self.models_dict = {x: accessed_models_map[x][1] for x in list(self.labels)}

    def test_complaints_creation_view(self):
        responses_list = []
        for obj in self.models_dict.items():
            label = obj[0]
            model = obj[1]
            response = self.client.hx_post(
                reverse('complaints:complaint-create', args=(label, model.objects.first().uuid))
            )
            responses_list.append(response.status_code)
        self.assertTrue(all(status in [200, 201] for status in responses_list))

    def test_invalid_model_complaints_creation_view(self):
        tf = TheoristFriendship.objects.first()
        fuzzy_model = ComplaintFactory.create(content_object=tf)
        response = self.client.hx_post(
            reverse('complaints:complaint-create', args=(self.fake.slug(), fuzzy_model.uuid))
        )
        self.assertFormError(response.context['form'], None, [_('Invalid object to complaint.')])
