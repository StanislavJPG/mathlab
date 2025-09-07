from django.urls import path

from server.apps.game_area.logic.quizzes import (
    MathQuizPlayBlocksListView,
    MathQuizBaseQuizView,
    MathQuizGameMenuView,
    MathQuizFinishDetailView,
)

app_name = 'quizzes'

urlpatterns = [
    path('', MathQuizPlayBlocksListView.as_view(), name='hx-mathquiz-playblocks'),
    path('<uuid:uuid>/play/', MathQuizBaseQuizView.as_view(), name='mathquiz-base'),
    path('hx/<uuid:quiz_uuid>/<int:pk>/start-play/', MathQuizGameMenuView.as_view(), name='hx-mathquiz-start-play'),
    path('<uuid:uuid>/finish-quiz/', MathQuizFinishDetailView.as_view(), name='hx-mathquiz-finish-quiz'),
]
