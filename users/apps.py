from django.apps import AppConfig
from django.db.models.signals import pre_save


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # def ready(self):
    #     from users.models import rank_creator, CustomUser
    #     pre_save.connect(rank_creator, sender=CustomUser)
