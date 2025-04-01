from django.db import models
from django.db.models import UniqueConstraint
from django_lifecycle import LifecycleModel

from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class TheoristChatRoom(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    first_member = models.ForeignKey(
        'theorist.Theorist', related_name='chat_rooms_initiated', null=True, on_delete=models.SET_NULL
    )
    second_member = models.ForeignKey(
        'theorist.Theorist', related_name='chat_rooms_received', null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.first_member.full_name} and {self.second_member.full_name} | {self.__class__.__name__} | id - {self.id}'

    class Meta:
        constraints = [UniqueConstraint(fields=['first_member', 'second_member'], name='%(app_label)s_unique_members')]
        verbose_name = 'Theorist Chat Room'
        verbose_name_plural = 'Theorist Chat Rooms'


class TheoristMessage(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    message = models.TextField(max_length=500)
    sender = models.ForeignKey('theorist.Theorist', related_name='messages', null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey('theorist_chat.TheoristChatRoom', on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'{self.sender.full_name} | {self.__class__.__name__} | id - {self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Theorist Message'
        verbose_name_plural = 'Theorist Messages'
