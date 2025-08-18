from django.apps import AppConfig


class GameAreaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.game_area'

    def ready(self):
        pass
