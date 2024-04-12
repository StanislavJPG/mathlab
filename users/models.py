from django.db import models
from django.contrib.auth.models import AbstractUser


class Image(models.Model):
    image = models.CharField('image', max_length=255, null=False)


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField("email address", blank=True, unique=True)
    score = models.IntegerField('score', null=False, default=0)
    image = models.ForeignKey(Image,
                              on_delete=models.CASCADE,
                              null=True)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ('username',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.username}'
