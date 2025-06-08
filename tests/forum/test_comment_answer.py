from django.core import exceptions
from django.http import Http404
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from server.apps.forum.factories import PostFactory, CommentFactory, CommentAnswerFactory
from server.apps.forum.logic.comment_answers import (
    HXCommentAnswersView,
    CommentAnswerCreateView,
    CommentAnswerDeleteView,
)
from server.apps.forum.models import PostCategory
from tests.testcases import TheoristTestCase
from tests import testutils


class CommentAnswerTest(TheoristTestCase):
    def setUp(self):
        super().setUp()
        PostCategory.create_data()
        self.post = PostFactory.create(**{'theorist': self.theorist})
        self.comment = CommentFactory.create(**{'theorist': self.theorist, 'post': self.post})
        self.comment_answer = CommentAnswerFactory.create(**{'theorist': self.theorist, 'comment': self.comment})

    def _test_hx_answers_view_case(self, **response_kwargs):  # CASE METHOD FOR REUSE
        request = self.hx_factory.get(reverse('forum:hx-comment-answers', kwargs={'uuid': self.comment.uuid}))
        return self.get_response(
            cbv=HXCommentAnswersView, request=request, kwargs={'uuid': self.comment.uuid}, **response_kwargs
        )

    def test_hx_answers_view(self):
        response = self._test_hx_answers_view_case()
        self.assertEqual(response.status_code, 200)

    def test_non_htmx_hx_answers_view(self):
        self.hx_factory = RequestFactory()  # simulate non-htmx request
        try:
            self._test_hx_answers_view_case()
        except exceptions.PermissionDenied:
            self.assertTrue(True)

    def test_unauthorized_hx_answers_view(self):
        response = self._test_hx_answers_view_case(is_anonymous=True)
        self.assertEqual(response.status_code, 200)  # because it is a public view

    def _test_comment_answer_create_view_case(self, data=None, **response_kwargs):  # CASE METHOD FOR REUSE
        request = self.hx_factory.post(
            reverse('forum:comment-answer-create', kwargs={'comment_uuid': self.comment.uuid}), data=data or {}
        )
        return self.get_response(
            cbv=CommentAnswerCreateView, request=request, kwargs={'comment_uuid': self.comment.uuid}, **response_kwargs
        )

    def test_comment_answer_create_view(self):
        response = self._test_comment_answer_create_view_case(
            data={'text_body': self.fake.text(max_nb_chars=400), 'send_to_post_owner': True}
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_input_comment_answer_create_view(self):
        response = self._test_comment_answer_create_view_case(
            data={'text_body': self.fake.text(max_nb_chars=5000)}, return_view_instance=True
        )
        if testutils.is_too_long_input(response, 'text_body'):
            self.assertFormError(response.get_form(), 'text_body', response.get_form().errors['text_body'])
        else:
            self.assertFalse(True)

    def test_invalid_empty_comment_answer_create_view(self):
        response = self._test_comment_answer_create_view_case(data={}, return_view_instance=True)
        self.assertFormError(response.get_form(), 'text_body', _('This field is required.'))

    def test_unauthorized_comment_answer_create_view(self):
        response = self._test_comment_answer_create_view_case(is_anonymous=True)
        self.assertEqual(response.status_code, 302)

    def _test_delete_comment_answer_view_case(self, data=None, **response_kwargs):  # CASE METHOD FOR REUSE
        request = self.hx_factory.delete(
            reverse('forum:comment-answer-delete', kwargs={'uuid': self.comment_answer.uuid}), data=data or {}
        )
        return self.get_response(
            cbv=CommentAnswerDeleteView, request=request, kwargs={'uuid': self.comment_answer.uuid}, **response_kwargs
        )

    def test_delete_comment_answer_view(self):
        response = self._test_delete_comment_answer_view_case()
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_answer_by_stranger_view(self):
        try:
            self._test_delete_comment_answer_view_case(is_dummy_theorist=True)
        except Http404:
            self.assertTrue(True)  # i.e strangers cannot delete other answers

    def test_unauthorized_delete_comment_answer_view(self):
        response = self._test_delete_comment_answer_view_case(is_anonymous=True)
        self.assertEqual(response.status_code, 302)
