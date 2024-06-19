from __future__ import annotations
from datetime import datetime

from rest_framework import serializers

from .models import Post, Category, Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    likes_count = serializers.IntegerField(required=False)
    dislikes_count = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        exclude = ('likes', 'dislikes')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['modified_at']:
            representation['modified_at'] = datetime.fromisoformat(representation['modified_at'])
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        return representation

    def validate(self, attrs):
        if len(attrs['comment']) >= 15:
            return attrs
        raise serializers.ValidationError('Length must be more than 15')

    def create(self, validated_data):
        post = Post.objects.select_related('user').get(pk=validated_data['post'].id)
        user = self.context['request'].user
        return Comment.objects.create(comment=validated_data['comment'],
                                      post=post, user=user)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    categories = CategorySerializer(many=True)
    comments_quantity = serializers.IntegerField(required=False)
    likes = serializers.IntegerField(required=False)
    dislikes = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['modified_at'] = datetime.fromisoformat(representation['modified_at'])
        return representation


class CommentLastActionsSerializer(serializers.ModelSerializer):
    """
    the only goal of using this serializer is some cases
    instead of default CommentSerializer
    it's reduce a quantity of database queries
    """
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['comm_id'] = representation['id']
        representation['title'] = representation['comment']
        return representation

