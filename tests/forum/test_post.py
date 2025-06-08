from random import choices

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from server.apps.forum.factories import PostFactory
from server.apps.forum.logic.post_management import (
    PostCreateView,
    PostContentUpdateView,
    PostTitleUpdateView,
    PostDeleteView,
)
from server.apps.forum.logic.posts import HXPostLikesAndDislikesView, PostSupportUpdateView, PostDefaultImageView
from server.apps.forum.models import PostCategory
from tests.testcases import TheoristTestCase


class PostTest(TheoristTestCase):
    def setUp(self):
        super().setUp()
        PostCategory.create_data()
        self.post = PostFactory.create(**{'theorist': self.theorist})

    def test_post_base_view(self):
        request = self.client.get(reverse('forum:base-forum-page'))
        self.assertEqual(request.status_code, 200)

    def test_post_list_view(self):
        request = self.client.get(reverse('forum:post-list'))
        self.assertEqual(request.status_code, 200)

    def test_post_detail_view(self):
        request = self.client.get(
            reverse('forum:post-details', kwargs={'pk': self.post.pk, 'slug': self.post.slug}),
        )
        self.assertEqual(request.status_code, 200)

    def test_post_likes_and_dislikes_get_view(self):
        kwargs = {'uuid': self.post.uuid}
        request = self.hx_factory.get(reverse('forum:hx-post-rate', kwargs=kwargs))
        response = self.get_response(cbv=HXPostLikesAndDislikesView, request=request, kwargs=kwargs)
        self.assertEqual(response.status_code, 200)

    def test_post_like_view(self):
        kwargs = {'uuid': self.post.uuid}
        request = self.hx_factory.post(reverse('forum:hx-post-rate', kwargs=kwargs) + '?like=true')
        response = self.get_response(cbv=HXPostLikesAndDislikesView, request=request, kwargs=kwargs)
        self.assertEqual(response.status_code, 200)

    def test_post_dislike_view(self):
        kwargs = {'uuid': self.post.uuid}
        request = self.hx_factory.post(reverse('forum:hx-post-rate', kwargs=kwargs))
        response = self.get_response(cbv=HXPostLikesAndDislikesView, request=request, kwargs=kwargs)
        self.assertEqual(response.status_code, 200)

    def test_post_support_update_view(self):
        request = self.hx_factory.post(
            reverse('forum:posts-support-update', kwargs={'uuid': self.post.uuid}),
        )
        response = self.get_response(
            cbv=PostSupportUpdateView, request=request, is_dummy_theorist=True, kwargs={'uuid': self.post.uuid}
        )
        self.assertEqual(response.status_code, 200)

    def test_post_default_image_view(self):
        request = self.hx_factory.get(reverse('forum:post-avatar', kwargs={'uuid': self.post.uuid}))
        response = self.get_response(cbv=PostDefaultImageView, request=request, kwargs={'uuid': self.post.uuid})
        self.assertEqual(response.status_code, 200)

    def test_post_creation_view(self):
        request = self.hx_factory.post(
            reverse('forum:hx-post-create'),
            data={
                'title': self.fake.sentence(nb_words=5),
                'content': self.fake.text(max_nb_chars=2000),
                'theorist': self.theorist,
                'categories': choices(PostCategory.objects.all(), k=3),
            },
        )
        response = self.get_response(cbv=PostCreateView, request=request)

        self.assertEqual(response.status_code, 200)

    def test_post_unauthorized_creation_view(self):
        request = self.hx_factory.post(
            reverse('forum:hx-post-create'),
            data={
                'title': self.fake.sentence(nb_words=5),
                'content': self.fake.text(max_nb_chars=2000),
                'theorist': self.theorist,
                'categories': choices(PostCategory.objects.all(), k=3),
            },
        )
        response = self.get_response(cbv=PostCreateView, request=request, is_anonymous=True)

        self.assertEqual(response.status_code, 302)

    def test_post_content_update_view(self):
        post = self.post
        content_before = post.content
        request = self.hx_factory.post(
            reverse('forum:hx-post-content-update', kwargs={'uuid': post.uuid}),
            data={'content': self.fake.text(max_nb_chars=2000)},
        )
        response = self.get_response(cbv=PostContentUpdateView, request=request, kwargs={'uuid': post.uuid})
        post.refresh_from_db()
        content_after = post.content

        self.assertNotEqual(content_before, content_after)
        self.assertEqual(response.status_code, 200)

    def test_post_title_update_view(self):
        post = self.post
        title_before = post.title
        request = self.hx_factory.post(
            reverse('forum:hx-post-title-update', kwargs={'uuid': post.uuid}),
            data={'title': self.fake.sentence(nb_words=6)},
        )
        response = self.get_response(cbv=PostTitleUpdateView, request=request, kwargs={'uuid': post.uuid})
        post.refresh_from_db()
        title_after = post.title

        self.assertNotEqual(title_before, title_after)
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view(self):
        post = self.post
        request = self.hx_factory.delete(
            reverse('forum:post-delete', kwargs={'uuid': post.uuid}),
        )
        response = self.get_response(cbv=PostDeleteView, request=request, kwargs={'uuid': post.uuid})

        try:
            post.refresh_from_db()
            post_after = post
        except ObjectDoesNotExist:
            post_after = None

        self.assertIsNone(post_after)
        self.assertEqual(response.status_code, 200)

    def test_post_unauthorized_delete_view(self):
        post = self.post
        request = self.hx_factory.delete(
            reverse('forum:post-delete', kwargs={'uuid': post.uuid}),
        )
        response = self.get_response(cbv=PostDeleteView, request=request, is_anonymous=True, kwargs={'uuid': post.uuid})

        try:
            post.refresh_from_db()
            post_after = post
        except ObjectDoesNotExist:
            post_after = None

        self.assertIsNotNone(post_after)
        self.assertEqual(response.status_code, 302)
