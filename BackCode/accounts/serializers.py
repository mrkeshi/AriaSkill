from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.db.models import Q
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from activity.services import ActivityService
from notification.services import NotificationService as NS

from accounts.services.unique_username_for_email import unique_username_from_email
from accounts.services.normalize_url import normalize_url

User = get_user_model()

SOCIAL_FIELDS = (
    'instagram_link',
    'telegram_link',
    'discord_link',
    'linkedin_link',
)


def build_auth_response(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.avatar.url if user.avatar else None,
            'job_title': user.job_title,
            'about_me': user.about_me,
            'instagram_link': user.instagram_link,
            'telegram_link': user.telegram_link,
            'discord_link': user.discord_link,
            'linkedin_link': user.linkedin_link,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }
    }


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password_confirm')

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Passwords must match'})

        email = data.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user and user.is_active:
                raise serializers.ValidationError({'email': 'Email already registered and active'})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        email = validated_data.get('email')
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            return existing_user

        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop(self.username_field, None)
        self.fields['identifier'] = serializers.CharField(required=True)
        self.fields['password'] = serializers.CharField(write_only=True, required=True,
                                                        style={'input_type': 'password'})

    def validate(self, attrs):
        identifier = attrs.get("identifier", "").strip()
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError({'identifier': 'Identifier and password are required'})

        user = User.objects.filter(
            Q(email__iexact=identifier) | Q(username__iexact=identifier)
        ).first()

        if not user:
            raise serializers.ValidationError({'identifier': 'User not found'})

        if not user.is_active:
            raise serializers.ValidationError('user account is not active')

        authenticated_user = authenticate(
            request=self.context.get('request'),
            username=user.email,
            password=password
        )
        if not authenticated_user:
            ActivityService.login_failed(
                user,
                request=self.context.get('request'),
                identifier=identifier,
            )
            NS.login_failed(
                user,
                request=self.context.get('request'),
                identifier=identifier,
            )
            raise serializers.ValidationError('identifier or password error')

        ActivityService.login_success(
            authenticated_user,
            request=self.context.get('request'),
            method='password',
        )

        return build_auth_response(authenticated_user)


class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        google_client_id = settings.GOOGLE_CLIENT_ID
        if not google_client_id:
            raise serializers.ValidationError({'google': 'Google authentication is not configured.'})

        query = urlencode({'id_token': attrs['credential']})
        try:
            with urlopen(f'https://oauth2.googleapis.com/tokeninfo?{query}', timeout=10) as response:
                payload = json.loads(response.read().decode('utf-8'))
        except Exception:
            raise serializers.ValidationError({'credential': 'Invalid Google credential.'})

        if payload.get('aud') != google_client_id:
            raise serializers.ValidationError({'credential': 'Google credential audience is invalid.'})

        if payload.get('email_verified') not in (True, 'true', 'True'):
            raise serializers.ValidationError({'email': 'Google email is not verified.'})

        email = payload.get('email')
        if not email:
            raise serializers.ValidationError({'email': 'Google account email is missing.'})

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': unique_username_from_email(email),
                'first_name': payload.get('given_name', ''),
                'last_name': payload.get('family_name', ''),
                'is_active': True,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()
        elif not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        request = self.context.get('request')
        ActivityService.login_success(user, request=request, method='google')
        return build_auth_response(user)


class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'avatar',
            'job_title', 'about_me',
            'instagram_link', 'telegram_link', 'discord_link', 'linkedin_link',
            'is_staff', 'is_superuser',
        )

    def get_avatar(self, obj) -> str:
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    instagram_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    telegram_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    discord_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    linkedin_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'avatar',
            'job_title', 'about_me',
            'instagram_link', 'telegram_link', 'discord_link', 'linkedin_link',
        )

    def validate(self, attrs):
        for field in SOCIAL_FIELDS:
            if field in attrs:
                attrs[field] = normalize_url(attrs.get(field))
        return attrs


class AdminUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'avatar',
            'job_title', 'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'last_login',
        )
        read_only_fields = fields

    def get_avatar(self, obj) -> str:
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        return None


class AdminUserStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)


class AdminUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Passwords must match'})

        validate_password(password, self.context.get('user'))
        return attrs


class PublicProjectMiniSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    project_type_display = serializers.SerializerMethodField()
    download_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        from projects.models import Project
        model = Project
        fields = (
            'id', 'title', 'slug', 'image',
            'project_type', 'project_type_display',
            'likes_count', 'download_count', 'view_count',
            'created_at', 'skills',
        )

    def get_skills(self, obj):
        return [
            {
                'id': s.id,
                'name': s.name,
                'slug': s.slug,
                'icon': s.icon.url if s.icon else None,
            }
            for s in obj.skills.all()[:4]
        ]

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None

    def get_project_type_display(self, obj):
        return obj.get_project_type_display()

    def get_download_count(self, obj) -> int:
        return obj.download_logs.count()

    def get_view_count(self, obj) -> int:
        return obj.view_logs.count()


class PublicUserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username', 'full_name', 'first_name', 'last_name', 'avatar',
            'job_title', 'about_me',
            'instagram_link', 'telegram_link', 'discord_link', 'linkedin_link',
            'date_joined',
            'projects', 'total_likes', 'projects_count',
        )

    def get_avatar(self, obj):
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        return None

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'.strip() or obj.username

    def get_projects(self, obj):
        from projects.models import Project
        qs = (
            Project.objects
            .filter(user=obj, status='approved')
            .prefetch_related('skills')
            .order_by('-created_at')
        )
        return PublicProjectMiniSerializer(qs, many=True).data

    def get_total_likes(self, obj):
        from django.db.models import Sum
        from projects.models import Project
        result = Project.objects.filter(user=obj, status='approved').aggregate(
            total=Sum('likes_count')
        )
        return result['total'] or 0

    def get_projects_count(self, obj):
        from projects.models import Project
        return Project.objects.filter(user=obj, status='approved').count()