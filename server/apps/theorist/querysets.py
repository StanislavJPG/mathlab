from django.db import models
from django.db.models import Q

from server.apps.theorist.choices import TheoristFriendshipStatusChoices


class TheoristQuerySet(models.QuerySet):
    def filter_by_accepted_friendship_as_member(self, member):
        return self.filter(
            (
                Q(friendship_requester__requester=member)
                & Q(friendship_requester__status=TheoristFriendshipStatusChoices.ACCEPTED)
            )
            | (
                Q(friendship_receiver__receiver=member)
                & Q(friendship_receiver__status=TheoristFriendshipStatusChoices.ACCEPTED)
            )
            | (
                Q(friendship_requester__receiver=member)
                & Q(friendship_requester__status=TheoristFriendshipStatusChoices.ACCEPTED)
            )
            | (
                Q(friendship_receiver__requester=member)
                & Q(friendship_receiver__status=TheoristFriendshipStatusChoices.ACCEPTED)
            )
        )

    def filter_by_is_onboarded(self):
        return self.filter(is_onboarded=True)

    def filter_is_able_to_get_messages(self):
        return self.filter(settings__is_able_to_get_messages=True)

    def filter_is_chats_available(self):
        return self.filter(chat_configuration__is_chats_available=True)


class TheoristFriendshipQuerySet(models.QuerySet):
    def filter_by_accepted_status(self):
        return self.filter(status=TheoristFriendshipStatusChoices.ACCEPTED)

    def filter_by_rejected_status(self):
        return self.filter(status=TheoristFriendshipStatusChoices.REJECTED)

    def filter_by_pending_status(self):
        return self.filter(status=TheoristFriendshipStatusChoices.PENDING)
