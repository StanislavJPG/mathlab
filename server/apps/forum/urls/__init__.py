from .post_urls import urlpatterns as post_urls
from .comment_urls import urlpatterns as comment_urls
from .answer_urls import urlpatterns as answer_urls

urlpatterns = post_urls + comment_urls + answer_urls
