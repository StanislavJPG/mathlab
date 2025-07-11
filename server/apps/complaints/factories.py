from factory.base import T

import factory
from django.contrib.contenttypes.models import ContentType
from factory import fuzzy

from server.apps.complaints.choices import ComplaintCategoryChoices


class ComplaintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'complaints.Complaint'

    complaint_text = factory.Faker('text', max_nb_chars=250)
    category = fuzzy.FuzzyChoice(ComplaintCategoryChoices.choices, getter=lambda x: x[0])

    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute('content_object.id')
    content_object = None

    @classmethod
    def create(cls, content_object, **kwargs) -> T:
        return super().create(content_object=content_object, **kwargs)
