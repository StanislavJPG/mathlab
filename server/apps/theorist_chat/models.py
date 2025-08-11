import django_bleach.models as bleach

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse
from django.utils import timezone

from django_lifecycle import LifecycleModel, hook, BEFORE_CREATE
from django_page_resolver.models import PageResolverModel
from dynamic_filenames import FilePattern

from server.apps.theorist_chat.querysets import TheoristChatRoomQuerySet, TheoristMessageQueryset
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin
from server.common.utils.helpers import format_relative_time
from server.common.validators import validate_audio_ext, validate_media_ext


class TheoristChatGroupConfiguration(UUIDModelMixin, TimeStampedModelMixin):
    theorist = models.OneToOneField('theorist.Theorist', on_delete=models.CASCADE, related_name='chat_configuration')
    is_chats_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.theorist.full_name} | {self.__class__.__name__} | id - {self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Theorist Chat Group Configurations'
        verbose_name = 'Theorist Chat Group Configuration'


class TheoristChatRoom(UUIDModelMixin, TimeStampedModelMixin, PageResolverModel, LifecycleModel):
    first_member = models.ForeignKey(
        'theorist.Theorist', related_name='chat_rooms_initiated', null=True, on_delete=models.SET_NULL
    )
    second_member = models.ForeignKey(
        'theorist.Theorist', related_name='chat_rooms_received', null=True, on_delete=models.SET_NULL
    )
    last_sms_sent_at = models.DateTimeField(null=True)

    objects = TheoristChatRoomQuerySet.as_manager()

    def __str__(self):
        first_member = getattr(self.first_member, 'full_name', 'None person')
        second_member = getattr(self.second_member, 'full_name', 'None person')
        return f'{first_member} and {second_member} | {self.__class__.__name__} | id - {self.id}'

    class Meta:
        constraints = [UniqueConstraint(fields=['first_member', 'second_member'], name='%(app_label)s_unique_members')]
        verbose_name = 'Theorist Chat Room'
        verbose_name_plural = 'Theorist Chat Rooms'

    def clean(self, *args, **kwargs):
        if self.first_member == self.second_member:
            raise ValidationError('Cannot assign the same members')

    def get_absolute_url(self, next_uuid, mailbox_page=1):
        # next_uuid is room uuid to be opened after url opening
        return reverse('forum:theorist_chat:chat-base-page') + f'?next_uuid={next_uuid}&page={mailbox_page}'

    @classmethod
    def get_room(cls, *members):  # Members order is not important
        if len(members) == 2:
            first_list = TheoristChatRoom.objects.filter(first_member=members[0], second_member=members[1]).values_list(
                'id', flat=True
            )
            second_list = TheoristChatRoom.objects.filter(
                first_member=members[1], second_member=members[0]
            ).values_list('id', flat=True)

            ids = [*first_list, *second_list]
            return TheoristChatRoom.objects.filter(id__in=ids).first()

    @property
    def is_any_of_members_blocked_another(self):
        blocked_by_first = (
            self.first_member.blacklist.blocked_theorists.filter(id=self.second_member_id).exists()
            if self.first_member
            else False
        )
        blocked_by_second = (
            self.second_member.blacklist.blocked_theorists.filter(id=self.first_member_id).exists()
            if self.second_member
            else False
        )

        return any((blocked_by_first, blocked_by_second))


audio_upload_to_path = FilePattern(
    filename_pattern='{app_label:.25}/rooms/{instance.room.uuid}/{instance.sender.full_name_slug}/audio/{uuid:s}{ext}'
)

media_upload_to_path = FilePattern(
    filename_pattern='{app_label:.25}/rooms/{instance.room.uuid}/{instance.sender.full_name_slug}/media/{uuid:s}{ext}'
)


class TheoristMessage(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    message = bleach.BleachField(max_length=500, blank=True)
    audio_message = models.FileField(
        upload_to=audio_upload_to_path, validators=[validate_audio_ext], null=True, blank=True
    )
    media_message = models.FileField(
        upload_to=media_upload_to_path,
        validators=[validate_media_ext],
        null=True,
        blank=True,
    )

    sender = models.ForeignKey('theorist.Theorist', related_name='messages', null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey('theorist_chat.TheoristChatRoom', on_delete=models.CASCADE, related_name='messages')

    replied_to = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.SET_NULL)

    was_safe_deleted_by = models.ForeignKey(
        'theorist.Theorist', null=True, blank=True, on_delete=models.SET_NULL, related_name='deleted_messages'
    )
    is_safe_deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    is_system = models.BooleanField(default=False)

    objects = TheoristMessageQueryset.as_manager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Theorist Message'
        verbose_name_plural = 'Theorist Messages'

    def __str__(self):
        return f'{self.sender.full_name} | {self.__class__.__name__} | id - {self.id}'

    def clean(self):
        if self.sender_id not in [self.room.first_member_id, self.room.second_member_id]:
            raise ValidationError('Sender needs to be a member in the following room.')
        if self.message and self.audio_message:
            raise ValidationError('Message needs to be specified whether audio or text.')

    def get_absolute_room_url(self, next_uuid, mailbox_page=1):
        # next_uuid is room uuid to be opened after url opening
        return reverse('forum:theorist_chat:chat-base-page') + f'?next_uuid={next_uuid}&page={mailbox_page}'

    @hook(BEFORE_CREATE)
    def before_create(self):
        self.room.last_sms_sent_at = timezone.now()
        self.room.save(update_fields=['last_sms_sent_at'])

    def safe_delete(self, deleted_by=None):
        self.was_safe_deleted_by = deleted_by if deleted_by else self.sender
        self.is_safe_deleted = True
        self.save(update_fields=['was_safe_deleted_by', 'is_safe_deleted'])

    def recover_after_safe_delete(self):
        self.was_safe_deleted_by = None
        self.is_safe_deleted = False
        self.save(update_fields=['was_safe_deleted_by', 'is_safe_deleted'])

    @property
    def chat_convenient_created_at(self):
        return format_relative_time(self.created_at)
