from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Rang(models.Model):
    rang_title = models.CharField('rang title', max_length=30)

    def __str__(self):
        return f'{self.rang_title}'


class Score(models.Model):
    score = models.IntegerField('score')
    rang = models.ForeignKey(Rang, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.score}'


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField("email address", blank=True, unique=True)
    score = models.ForeignKey(
        Score,
        on_delete=models.CASCADE,
        null=True
    )
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.username}'
