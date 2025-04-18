import django_bleach.models as bleach

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_lifecycle import LifecycleModel, hook, BEFORE_CREATE

from server.apps.theorist_chat.managers import TheoristChatRoomQuerySet
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin


class TheoristChatGroupConfiguration(UUIDModelMixin, TimeStampedModelMixin):
    theorist = models.OneToOneField('theorist.Theorist', on_delete=models.CASCADE, related_name='chat_configuration')
    is_chats_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.theorist.full_name} | {self.__class__.__name__} | id - {self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Theorist Chat Group Configurations'
        verbose_name = 'Theorist Chat Group Configuration'


class TheoristChatRoom(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    first_member = models.ForeignKey(
        'theorist.Theorist', related_name='chat_rooms_initiated', null=True, on_delete=models.SET_NULL
    )
    second_member = models.ForeignKey(
        'theorist.Theorist', related_name='chat_rooms_received', null=True, on_delete=models.SET_NULL
    )
    last_sms_sent_at = models.DateTimeField(null=True)

    objects = TheoristChatRoomQuerySet.as_manager()

    def __str__(self):
        return f'{self.first_member.full_name} and {self.second_member.full_name} | {self.__class__.__name__} | id - {self.id}'

    class Meta:
        constraints = [UniqueConstraint(fields=['first_member', 'second_member'], name='%(app_label)s_unique_members')]
        verbose_name = 'Theorist Chat Room'
        verbose_name_plural = 'Theorist Chat Rooms'

    def clean(self, *args, **kwargs):
        if self.first_member == self.second_member:
            raise ValidationError('Cannot assign the same members')


class TheoristMessage(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    message = bleach.BleachField(max_length=500)
    sender = models.ForeignKey('theorist.Theorist', related_name='messages', null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey('theorist_chat.TheoristChatRoom', on_delete=models.CASCADE, related_name='messages')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Theorist Message'
        verbose_name_plural = 'Theorist Messages'

    def __str__(self):
        return f'{self.sender.full_name} | {self.__class__.__name__} | id - {self.id}'

    @hook(BEFORE_CREATE)
    def before_create(self):
        self.room.last_sms_sent_at = timezone.now()
        self.room.save(update_fields=['last_sms_sent_at'])

    @property
    def chat_convenient_created_at(self):
        t = timezone.now() - self.created_at
        sent = t.seconds
        if sent <= 30:
            return _('Just now')
        elif 60 <= sent <= 300:
            return _('Couple minutes ago')
        elif 300 < sent <= 400:
            return _('5 minutes ago')
        elif t.days < 1:
            return self.created_at.time()
        else:
            return self.created_at
