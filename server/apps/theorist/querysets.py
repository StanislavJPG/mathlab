from django.db import models

from server.apps.theorist.choices import TheoristFriendshipStatusChoices


class TheoristFriendshipQuerySet(models.QuerySet):
    def filter_by_accepted_status(self):
        return self.filter(status=TheoristFriendshipStatusChoices.ACCEPTED)

    def filter_by_rejected_status(self):
        return self.filter(status=TheoristFriendshipStatusChoices.REJECTED)

    def filter_by_pending_status(self):
        return self.filter(status=TheoristFriendshipStatusChoices.PENDING)
