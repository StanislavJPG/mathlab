from datetime import datetime

from rest_framework import serializers

from chat.models import Message
from users.models import CustomUser


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sender']: str = CustomUser.objects.get(id=representation['sender']).username
        representation['sent_at'] = datetime.fromisoformat(representation['sent_at'])
        return representation
