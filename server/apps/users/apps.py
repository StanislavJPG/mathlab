from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.users"

    # def ready(self):
    #     from users.models import rank_creator, CustomUser
    #     pre_save.connect(rank_creator, sender=CustomUser)
