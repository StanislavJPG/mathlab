from allauth.account.models import EmailAddress
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import Theorist


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.email} | {self.__class__.__name__} | id - {self.id}'

    def create_initial_theorist(self):
        if not hasattr(self, 'theorist'):
            return Theorist.objects.create(full_name=self.username, user=self)

    @property
    def is_email_verified(self) -> bool:
        return EmailAddress.objects.get(email=self.email).verified
