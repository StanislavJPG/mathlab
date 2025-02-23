from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.email} | {self.__class__.__name__} | id - {self.id}'

    # def update_rank(self):
    #     if self.score < 50:
    #         self.rank = self.JUNIOR
    #     elif 50 <= self.score < 100:
    #         self.rank = self.OLYMPIC
    #     elif 100 <= self.score < 200:
    #         self.rank = self.TEACHER
    #     elif 200 <= self.score < 600:
    #         self.rank = self.GURU
    #     else:
    #         self.rank = self.MATH_LORD
    #     self.save()
