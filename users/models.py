from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField("email address", blank=True, unique=True)
    score = models.IntegerField('score', null=False, default=0)
    rank = models.CharField(verbose_name='rank', max_length=150, null=False, default='Учень математики')

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ('username',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.username}'


class ProfileImage(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mathlab/templates/static/profile_pics', blank=True)

    def __str__(self):
        return f'{self.user}'


def rank_creator(sender, instance, **kwargs) -> None:
    if instance.score < 50:
        instance.rank = 'Учень математики'

    elif 50 <= instance.score < 100:
        instance.rank = 'Олімпіадник'

    elif 100 <= instance.score < 200:
        instance.rank = 'Вчитель математики'

    elif 200 <= instance.score < 600:
        instance.rank = 'Гуру математики'

    else:
        instance.rank = 'Володар математики'
