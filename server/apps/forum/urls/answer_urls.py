from django.urls import path

from server.apps.forum.logic.comment_answers import HXCommentAnswerDetailView, CommentAnswerCreateView

urlpatterns = [
    path(
        'hx/answers/<uuid:uuid>/',
        HXCommentAnswerDetailView.as_view(),
        name='hx-comment-answers',
    ),
    path(
        '<uuid:uuid>/comments/answers/create/',
        CommentAnswerCreateView.as_view(),
        name='comment-answer-create',
    ),
]
