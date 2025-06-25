from django.views.generic import TemplateView


class TheoristCommunityBaseTemplateView(TemplateView):
    template_name = 'base_community_list.html'
