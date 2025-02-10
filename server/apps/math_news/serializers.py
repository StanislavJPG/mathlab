from rest_framework import serializers

from server.apps.math_news.models import MathNews


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MathNews
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["title"]: str = representation["title"].replace("\n", " ")
        return representation
