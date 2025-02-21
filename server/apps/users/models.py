from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField('email address', blank=True, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.username}'

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
