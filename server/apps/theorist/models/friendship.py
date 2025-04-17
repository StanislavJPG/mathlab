import typing

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel, hook, BEFORE_UPDATE
from typing_extensions import assert_never

from server.apps.theorist.choices import TheoristFriendshipStatusChoices
from server.common.mixins.models import UUIDModelMixin, TimeStampedModelMixin

if typing.TYPE_CHECKING:
    from server.apps.theorist.models import Theorist


class TheoristFriendship(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    PredefinedFriendship = TheoristFriendshipStatusChoices

    # requester is the person who asks receiver for the friendship
    requester = models.ForeignKey('theorist.Theorist', on_delete=models.CASCADE, related_name='friendship_requester')
    # receiver is the person who was requested for the friendship by requester
    receiver = models.ForeignKey('theorist.Theorist', on_delete=models.CASCADE, related_name='friendship_receiver')

    status = models.CharField(choices=PredefinedFriendship, default=PredefinedFriendship.PENDING)

    # additional time-check field
    status_changed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-status_changed_at', '-created_at')
        constraints = [UniqueConstraint(fields=['receiver', 'requester'], name='%(app_label)s_unique_members')]
        verbose_name = _('Friendship')
        verbose_name_plural = _('Friendships')

    def __str__(self):
        return f'Requester - {self.requester} | Receiver - {self.receiver} | {self.__class__.__name__} | id - {self.id}'

    def clean(self):
        if self.requester == self.receiver:
            raise ValidationError('Requester and receiver must be different.')

        if not self.pk:
            if TheoristFriendship.objects.filter(
                Q(requester=self.receiver, receiver=self.requester)
                | Q(requester=self.requester, receiver=self.receiver)
            ).exists():
                raise ValidationError('Request already exists in the opposite direction.')

    @hook(BEFORE_UPDATE, when='status', has_changed=True)
    def after_update(self):
        self.status_changed_at = timezone.now()

    @property
    def convenience_status_for_requester(self):
        if self.status == self.PredefinedFriendship.PENDING:
            return _('%s still examines yours friendship...') % self.receiver
        elif self.status == self.PredefinedFriendship.REJECTED:
            return _('%s has rejected your friendship request!') % self.receiver
        elif self.status == self.PredefinedFriendship.ACCEPTED:
            return _('%s has accepted your friendship request!') % self.receiver
        else:
            assert_never(self.status)

    @classmethod
    def create_friendship_request(cls, from_: 'Theorist', to: 'Theorist'):
        return cls.objects.create(
            requester=from_,
            receiver=to,
        )

    def accept_friendship_request(self):
        self.status = self.PredefinedFriendship.ACCEPTED
        self.save(update_fields=['status', 'status_changed_at'])  # status_changed_at to commit hook changes

    def reject_friendship_request(self):
        self.status = self.PredefinedFriendship.REJECTED
        self.save(update_fields=['status', 'status_changed_at'])  # status_changed_at to commit hook changes


class TheoristFriendshipBlackList(UUIDModelMixin, TimeStampedModelMixin, LifecycleModel):
    owner = models.OneToOneField('theorist.Theorist', on_delete=models.CASCADE, related_name='blacklist')
    blocked_theorists = models.ManyToManyField('theorist.Theorist', related_name='blacklisted_by')

    class Meta:
        verbose_name = _('Blacklist')
        verbose_name_plural = _('Blacklists')

    def __str__(self):
        return f'{self.owner} | {self.__class__.__name__} | id - {self.id}'
