from __future__ import annotations

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from users.models import CustomUser as User, ProfileImage


class ProfileSerializer:
    @staticmethod
    def get_profile_image(user_pk):
        try:
            cached_data = cache.get(f'user_image.{user_pk}')
            if not cached_data:
                profile_image = ProfileImage.objects.filter(user__pk=user_pk).values('image').get()
                cache.set(f'user_image.{user_pk}', profile_image, 600)
            else:
                profile_image = cached_data

            return profile_image['image'].split('/')[-1]
        except ObjectDoesNotExist:
            return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rank'] = instance.rank.rank
        return representation
