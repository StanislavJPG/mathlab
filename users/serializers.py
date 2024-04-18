from __future__ import annotations

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from forum.service import rank_creator_for_serializer
from users.models import CustomUser as User, ProfileImage


class ProfileSerializer:
    @staticmethod
    def get_profile_image(user_pk):
        try:
            profile_image = ProfileImage.objects.filter(user__pk=user_pk).values('image').get()
            return profile_image['image'].split('/')[-1]
        except ObjectDoesNotExist:
            return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rank'] = rank_creator_for_serializer(representation)
        return representation
