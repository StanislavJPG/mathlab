from django.apps import AppConfig
from django.core.signals import request_finished


class GameAreaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.game_area'

    def ready(self):
        from . import signals

        request_finished.connect(signals.update_mathquiz_avg_time)
