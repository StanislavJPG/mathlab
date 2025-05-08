from django.db import models


class CarouselQuerySet(models.QuerySet):
    def filter_by_is_active(self):
        return self.filter(is_active=True)
