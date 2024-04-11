from rest_framework import serializers

from users.models import Rang, Score, CustomUser as User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rang
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
