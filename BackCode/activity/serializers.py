from rest_framework import serializers

from activity.models import Activity, ActivityType


class ActivitySerializer(serializers.ModelSerializer):
    related_project_title = serializers.CharField(source='related_project.title', read_only=True)
    related_project_slug = serializers.CharField(source='related_project.slug', read_only=True)
    related_user_username = serializers.CharField(source='related_user.username', read_only=True)

    class Meta:
        model = Activity
        fields = (
            'id', 'user_id', 'type', 'title', 'description',
            'related_project_id', 'related_project_title', 'related_project_slug',
            'related_user_id', 'related_user_username', 'metadata',
            'is_seen', 'created_at', 'updated_at',
        )
        read_only_fields = fields


class ActivityMarkSeenSerializer(serializers.Serializer):
    is_seen = serializers.BooleanField(required=False, default=True)


class ActivityFilterSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=ActivityType.choices, required=False)
    is_seen = serializers.BooleanField(required=False)
