from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from server.apps.forum.factories import CommentFactory, PostFactory
from server.apps.forum.logic.comment_management import CommentCreateView, CommentUpdateView, CommentDeleteView
from server.apps.forum.logic.comments import (
    CommentListView,
    HXCommentQuantityView,
    HXCommentLikesAndDislikesView,
    CommentSupportUpdateView,
)
from server.apps.forum.models import PostCategory
from tests import testutils
from tests.testcases import TheoristTestCase


class CommentTest(TheoristTestCase):
    def setUp(self):
        super().setUp()
        PostCategory.create_data()
        self.post = PostFactory.create(**{'theorist': self.theorist})
        self.comment = CommentFactory.create(**{'theorist': self.theorist, 'post': self.post})

    def test_comment_list_view(self):
        request = self.hx_factory.get(reverse('forum:comments-block', kwargs={'post_uuid': self.post.uuid}))
        response = self.get_response(cbv=CommentListView, request=request, kwargs={'post_uuid': self.post.uuid})
        self.assertEqual(response.status_code, 200)

    def test_hx_comment_quantity_view(self):
        comments_count_before = self.post.comments.count()
        request = self.hx_factory.get(reverse('forum:comments-count', kwargs={'post_uuid': self.post.uuid}))
        response = self.get_response(cbv=HXCommentQuantityView, request=request, kwargs={'post_uuid': self.post.uuid})
        self.post.refresh_from_db()
        self.assertEqual(comments_count_before, self.post.comments_quantity)
        self.assertEqual(response.status_code, 200)

    def test_comment_likes_and_dislikes_get_view(self):
        kwargs = {'uuid': self.comment.uuid}
        request = self.hx_factory.get(reverse('forum:hx-comment-rate', kwargs=kwargs))
        response = self.get_response(cbv=HXCommentLikesAndDislikesView, request=request, kwargs=kwargs)
        self.assertEqual(response.status_code, 200)

    def test_comment_like_view(self):
        kwargs = {'uuid': self.comment.uuid}
        request = self.hx_factory.post(reverse('forum:hx-comment-rate', kwargs=kwargs) + '?like=true')
        response = self.get_response(cbv=HXCommentLikesAndDislikesView, request=request, kwargs=kwargs)
        self.assertEqual(response.status_code, 200)

    def test_comment_dislike_view(self):
        kwargs = {'uuid': self.comment.uuid}
        request = self.hx_factory.post(reverse('forum:hx-comment-rate', kwargs=kwargs))
        response = self.get_response(cbv=HXCommentLikesAndDislikesView, request=request, kwargs=kwargs)
        self.assertEqual(response.status_code, 200)

    def test_comment_support_update_view(self):
        request = self.hx_factory.post(
            reverse('forum:comments-support-update', kwargs={'uuid': self.comment.uuid}),
        )
        response = self.get_response(
            cbv=CommentSupportUpdateView, request=request, is_dummy_theorist=True, kwargs={'uuid': self.comment.uuid}
        )
        self.assertEqual(response.status_code, 200)

    def _test_comment_create_case(self, data=None, **response_kwargs):  # CASE METHOD FOR REUSE
        request = self.hx_factory.post(
            reverse('forum:comment-create', kwargs={'post_uuid': self.post.uuid}), data=data or {}
        )
        return self.get_response(
            cbv=CommentCreateView, request=request, kwargs={'post_uuid': self.post.uuid}, **response_kwargs
        )

    def test_valid_comment_create_view(self):
        response = self._test_comment_create_case(
            data={'comment': self.fake.text(max_nb_chars=2000)},
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_empty_comment_create_view(self):
        response = self._test_comment_create_case(return_view_instance=True)
        self.assertFormError(response.get_form(), 'comment', _('This field is required.'))

    def test_invalid_input_comment_create_view(self):
        response = self._test_comment_create_case(
            data={'comment': self.fake.text(max_nb_chars=15000)}, return_view_instance=True
        )

        if testutils.is_too_long_input(response, 'comment'):
            self.assertFormError(response.get_form(), 'comment', response.get_form().errors['comment'])
        else:
            self.assertFalse(True)

    def test_unauthorized_comment_create_view(self):
        response = self._test_comment_create_case(
            data={'comment': self.fake.text(max_nb_chars=15000)},
            is_anonymous=True,
        )
        self.assertEqual(response.status_code, 302)

    def test_comment_update_view(self):
        request = self.hx_factory.post(
            reverse('forum:comment-update', kwargs={'uuid': self.comment.uuid}),
            data={'predefined_comment': self.fake.text(max_nb_chars=2000)},
        )
        response = self.get_response(cbv=CommentUpdateView, request=request, kwargs={'uuid': self.comment.uuid})
        self.assertEqual(response.status_code, 200)

    def _test_comment_delete_case(self, data=None, **response_kwargs):  # CASE METHOD FOR REUSE
        kwargs = {'post_uuid': self.post.uuid, 'uuid': self.comment.uuid}
        request = self.hx_factory.delete(reverse('forum:comment-delete', kwargs=kwargs), data=data or {})
        return self.get_response(cbv=CommentDeleteView, request=request, kwargs=kwargs, **response_kwargs)

    def test_valid_comment_delete_view(self):
        response = self._test_comment_delete_case()
        self.assertEqual(response.status_code, 200)

    def test_post_delete_by_stranger_view(self):
        try:
            self._test_comment_delete_case(is_dummy_theorist=True)
        except Http404:
            self.assertTrue(True)  # i.e strangers cannot delete other answers

    def test_unauthorized_comment_delete_view(self):
        response = self._test_comment_delete_case(is_anonymous=True)
        self.assertEqual(response.status_code, 302)
