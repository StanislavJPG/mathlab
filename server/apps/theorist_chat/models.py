from django.db import models
from django_lifecycle import LifecycleModel

from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class TheoristMessagesGroup(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    first_member = models.ForeignKey('theorist.Theorist', null=True, on_delete=models.SET_NULL)
    second_member = models.ForeignKey('theorist.Theorist', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.first_member.full_name} and {self.second_member.full_name} | {self.__class__.__name__} | id - {self.id}'


class TheoristMessage(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    message = models.TextField(max_length=500)
    theorist = models.ForeignKey('theorist.Theorist', related_name='messages', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.theorist.full_name} | {self.__class__.__name__} | id - {self.id}'

    class Meta: ...
