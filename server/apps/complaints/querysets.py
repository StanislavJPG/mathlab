from django.db import models


class ComplaintQuerySet(models.QuerySet):
    def filter_by_processed(self):
        return self.filter(processed=True)

    def filter_by_not_processed(self):
        return self.filter(processed=False)
