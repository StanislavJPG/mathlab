from __future__ import annotations

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from users.models import CustomUser as User, ProfileImage


def rank_creator_for_serializer(representation: dict) -> str:
    user_content = representation['score']

    if user_content < 10:
        user_content = 'Учень математики'

    elif 10 <= user_content < 30:
        user_content = 'Олімпіадник'

    elif 30 <= user_content < 60:
        user_content = 'Вчитель математики'

    elif 60 <= user_content < 100:
        user_content = 'Гуру математики'

    else:
        user_content = 'Володар математики'

    return user_content


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
