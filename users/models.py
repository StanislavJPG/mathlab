from django.db import models
from django.contrib.auth.models import AbstractUser


class Rank(models.Model):
    rank = models.CharField(verbose_name='rank', max_length=150, null=False)


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField("email address", blank=True, unique=True)
    score = models.IntegerField('score', null=False, default=0)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, null=False, default=1)

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


def rank_creator(user_inst) -> None:
    if user_inst.score < 50:
        user_inst.rank = Rank.objects.get(pk=1)
    elif 50 <= user_inst.score < 100:
        user_inst.rank = Rank.objects.get(pk=2)
    elif 100 <= user_inst.score < 200:
        user_inst.rank = Rank.objects.get(pk=3)

    elif 200 <= user_inst.score < 600:
        user_inst.rank = Rank.objects.get(pk=4)
    else:
        user_inst.rank = Rank.objects.get(pk=5)
