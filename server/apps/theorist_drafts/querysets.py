from django.db import models


class TheoristDraftsConfigurationQuerySet(models.QuerySet):
    def filter_by_is_public_available(self):
        return self.filter(is_public_available=True)
