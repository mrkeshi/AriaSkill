from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Skill, Project, Comment

User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'slug', 'icon']
        read_only_fields = ['slug']


class UserBriefSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'avatar']

    def get_full_name(self, obj)->str:
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username

    def get_avatar(self, obj) -> str:
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            url = obj.avatar.url
            return request.build_absolute_uri(url) if request else url
        return ''


class ProjectSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        source='skills',
        write_only=True,
        required=False,
    )
    likes_count = serializers.IntegerField(read_only=True)
    download_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'image', 'file',
            'created_at', 'updated_at', 'user', 'likes_count', 'user_has_liked',
            'download_count', 'view_count',
            'comments_count', 'project_type', 'project_type_display', 'skills', 'skill_ids', 'status'
        ]
        read_only_fields = [
            'id', 'slug', 'created_at', 'updated_at', 'user',
            'likes_count', 'user_has_liked',
            'download_count', 'view_count',
            'comments_count', 'project_type_display', 'skills', 'status',
        ]

    def get_user_has_liked(self, obj) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_comments_count(self, obj) -> int:
        return obj.comments.filter(status='active', parent__isnull=True).count()

    def get_download_count(self, obj) -> int:
        return obj.download_logs.count()

    def get_view_count(self, obj) -> int:
        return obj.view_logs.count()


class ProjectStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)


class LikeResponseSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField(read_only=True)
    liked = serializers.BooleanField(read_only=True)


class DownloadCountSerializer(serializers.Serializer):
    download_count = serializers.IntegerField(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    user_avatar = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'project', 'user', 'user_name', 'user_avatar', 'message', 'status', 'parent', 'replies',
                  'created_at', 'updated_at',)
        read_only_fields = ('project', 'user', 'status', 'created_at', 'updated_at',)

    def get_replies(self, obj) -> list[dict]:
        replies = obj.replies.filter(status='active').select_related('user')
        if replies.exists():
            return CommentSerializer(replies, many=True, context=self.context).data
        return []

    def get_user_avatar(self, obj) -> str:
        request = self.context.get('request')
        if obj.user.avatar:
            url = obj.user.avatar.url
            return request.build_absolute_uri(url) if request else url
        return ''

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class CommentManagementSerializer(CommentSerializer):
    project_title = serializers.ReadOnlyField(source='project.title')
    project_slug = serializers.ReadOnlyField(source='project.slug')

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ('project_title', 'project_slug')
        read_only_fields = CommentSerializer.Meta.read_only_fields
