from django.urls import path

from server.apps.game_area.logic.quizzes import MathQuizPlayBlocksListView, MathQuizBaseQuizView, MathQuizStartPlayView

app_name = 'quizzes'

urlpatterns = [
    path('', MathQuizPlayBlocksListView.as_view(), name='hx-mathquiz-playblocks'),
    path('<uuid:uuid>/play/', MathQuizBaseQuizView.as_view(), name='mathquiz-base'),
    path('hx/<uuid:quiz_uuid>/<int:pk>/start-play/', MathQuizStartPlayView.as_view(), name='hx-mathquiz-start-play'),
]
