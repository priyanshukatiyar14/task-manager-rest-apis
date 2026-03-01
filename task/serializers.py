from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "username", "created_at", "updated_at"]