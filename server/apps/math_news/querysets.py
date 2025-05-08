from django.db import models


class MathNewsQueryset(models.QuerySet):
    def filter_by_is_visible(self):
        return self.filter(is_visible=True)
