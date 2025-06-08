from django.urls import path

from server.apps.forum.logic.comment_answers import (
    HXCommentAnswersView,
    CommentAnswerCreateView,
    CommentAnswerDeleteView,
)

urlpatterns = [
    path(
        'hx/answers/<uuid:uuid>/',
        HXCommentAnswersView.as_view(),
        name='hx-comment-answers',
    ),
    path(
        '<uuid:comment_uuid>/comments/answers/create/',
        CommentAnswerCreateView.as_view(),
        name='comment-answer-create',
    ),
    path(
        '<uuid:uuid>/comments/answers/delete/',
        CommentAnswerDeleteView.as_view(),
        name='comment-answer-delete',
    ),
]
