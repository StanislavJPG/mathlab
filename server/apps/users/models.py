from allauth.account.models import EmailAddress
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from server.apps.theorist.models import Theorist
from server.common.validators import username_validators


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=username_validators,
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )

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
