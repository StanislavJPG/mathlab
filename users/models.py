from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    JUNIOR = "JR"
    OLYMPIC = "OP"
    TEACHER = "TC"
    GURU = "GR"
    MATH_LORD = "LD"
    RANKS = (
        (JUNIOR, "Учень математики"),
        (OLYMPIC, "Олімпіадник"),
        (TEACHER, "Вчитель математики"),
        (GURU, "Гуру математики"),
        (MATH_LORD, "Володар математики")
    )

    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField("email address", blank=True, unique=True)
    score = models.IntegerField('score', null=False, default=0)
    rank = models.CharField('rank', choices=RANKS, max_length=2, default=JUNIOR)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ('username',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.username}'

    def update_rank(self):
        if self.score < 50:
            self.rank = self.JUNIOR
        elif 50 <= self.score < 100:
            self.rank = self.OLYMPIC
        elif 100 <= self.score < 200:
            self.rank = self.TEACHER
        elif 200 <= self.score < 600:
            self.rank = self.GURU
        else:
            self.rank = self.MATH_LORD
        self.save()


class ProfileImage(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='templates/static/profile_pics', blank=True)

    def __str__(self):
        return f'{self.user}'
