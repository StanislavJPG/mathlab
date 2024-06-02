from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Post, Category, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        post = instance

        representation['likes'] = post.post_likes.count()
        representation['dislikes'] = post.post_dislikes.count()
        representation['comments_quantity'] = Comment.objects.filter(post=instance.id).count()
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['modified_at'] = datetime.fromisoformat(representation['modified_at'])
        representation['categories'] = Category.objects.filter(pk__in=representation['categories'])
        representation['user'] = post.user
        return representation


class CommentLastActionsSerializer(serializers.ModelSerializer):
    """
    the only goal of using this serializer is some cases
    instead of default CommentSerializer
    it's reduce a quantity of database queries
    """

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comment = Comment.objects.get(pk=instance.id)
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['comm_id'] = representation['id']
        representation['post_title'] = comment.post.title
        representation['post_id'] = comment.post.id
        representation['title'] = representation['comment']
        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['modified_at']:
            representation['modified_at'] = datetime.fromisoformat(representation['modified_at'])
        comment = Comment.objects.get(pk=instance.id)

        representation['likes'] = comment.likes.count()
        representation['dislikes'] = comment.dislikes.count()
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['user_id'] = representation['user']
        representation['user'] = instance.user

        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
