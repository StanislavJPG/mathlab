from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin

from server.apps.forum.models.comment import Comment
from server.common.mixins.views import HXViewMixin


class HXCommentAnswerDetailView(HXViewMixin, MultipleObjectMixin, DetailView):
    model = Comment
    context_object_name = 'answers'
    template_name = 'comments/answers/answer_list.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'comment_uuid'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        object_list = self.object.answers.all()
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context
