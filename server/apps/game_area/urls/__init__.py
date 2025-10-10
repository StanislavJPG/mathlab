from django.urls import path, include

from server.apps.game_area.logic.gamearea import GameAreaTemplateView

app_name = 'gamearea'
urlpatterns = [
    path('', GameAreaTemplateView.as_view(), name='gamearea-base'),
    path('quizzes/', include('server.apps.game_area.urls.quizzes'), name='quizzes'),
]
