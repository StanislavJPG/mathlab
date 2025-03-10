from django.contrib import admin

from server.apps.forum.models import Comment, Post, PostCategory


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'likes_counter', 'dislikes_counter')
    list_filter = ('post', 'theorist')
    search_fields = ('id', 'uuid', 'post', 'user')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'comments_quantity')
    list_filter = ('theorist', 'title')


@admin.register(PostCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)
