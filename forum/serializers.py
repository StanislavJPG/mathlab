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
        post = Post.objects.get(pk=instance.id)
        representation['likes'] = post.post_likes.count()
        representation['dislikes'] = post.post_dislikes.count()
        representation['comments_quantity'] = len(Comment.objects.filter(post=representation['id']))
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['modified_at'] = datetime.fromisoformat(representation['modified_at'])
        representation['categories'] = Category.objects.filter(pk__in=representation['categories'])
        representation['user'] = (get_object_or_404(get_user_model(), pk=representation['user']),
                                  representation['user'])
        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['modified_at']:
            representation['modified_at'] = datetime.fromisoformat(representation['modified_at'])

        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['user'] = get_object_or_404(get_user_model(), pk=representation['user'])
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'