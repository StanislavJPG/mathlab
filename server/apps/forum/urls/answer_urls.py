from django.urls import path

from server.apps.forum.logic.comment_answers import HXCommentAnswerDetailView

urlpatterns = [
    path(
        'hx/answers/<uuid:comment_uuid>/',
        HXCommentAnswerDetailView.as_view(),
        name='hx-comment-answers',
    ),
]
