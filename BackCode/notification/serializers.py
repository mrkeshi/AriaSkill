from rest_framework import serializers

from notification.models import BroadcastLog, Notification, NotificationType


class NotificationSerializer(serializers.ModelSerializer):
    related_project_title = serializers.CharField(
        source='related_project.title', read_only=True
    )
    related_project_slug = serializers.CharField(
        source='related_project.slug', read_only=True
    )
    related_user_username = serializers.CharField(
        source='related_user.username', read_only=True
    )

    class Meta:
        model = Notification
        fields = (
            'id', 'type', 'title', 'message',
            'related_project_id', 'related_project_title', 'related_project_slug',
            'related_user_id', 'related_user_username',
            'metadata', 'is_read', 'created_at', 'updated_at',
        )
        read_only_fields = fields

class NotificationMarkReadSerializer(serializers.Serializer):
    is_read = serializers.BooleanField(required=False, default=True)

class NotificationFilterSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=NotificationType.choices, required=False)
    is_read = serializers.BooleanField(required=False)

class BroadcastSerializer(serializers.Serializer):
    title   = serializers.CharField(max_length=180, default='پیام همگانی')
    message = serializers.CharField(min_length=5)

class BroadcastLogSerializer(serializers.ModelSerializer):
    sent_by_username = serializers.CharField(
        source='sent_by.username', read_only=True, default='(حذف‌شده)'
    )

    class Meta:
        model  = BroadcastLog
        fields = (
            'id', 'title', 'message',
            'sent_by_id', 'sent_by_username',
            'sent_to_count', 'sent_at',
        )
        read_only_fields = fields
