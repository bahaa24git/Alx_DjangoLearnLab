from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Notification

User = get_user_model()


class ActorBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorBriefSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "actor", "verb", "timestamp", "is_read"]
