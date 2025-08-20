from django.urls import path

from server.apps.game_area.logic.quizzes import MathQuizPlayBlocksListView

app_name = 'quizzes'

urlpatterns = [
    path('', MathQuizPlayBlocksListView.as_view(), name='hx-mathquiz-playblocks'),
]
