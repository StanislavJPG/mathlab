from datetime import datetime

from rest_framework import serializers

from users.models import CustomUser
from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = datetime.fromisoformat(representation['created_at'])
        representation['categories'] = Category.objects.filter(pk__in=representation['categories'])
        representation['user'] = (CustomUser.objects.get(pk=representation['user']), representation['user'])
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
