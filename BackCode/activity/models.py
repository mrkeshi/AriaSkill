from django.conf import settings
from django.db import models
from django.utils import timezone


class ActivityType(models.TextChoices):
    LOGIN_SUCCESS = 'login_success', 'Login Success'
    LOGIN_FAILED = 'login_failed', 'Login Failed'
    PROJECT_PUBLISHED = 'project_published', 'Project Published'
    PROJECT_CREATED = 'project_created', 'Project Created'
    PROJECT_UPDATED = 'project_updated', 'Project Updated'
    PROJECT_DELETED = 'project_deleted', 'Project Deleted'
    PASSWORD_CHANGED = 'password_changed', 'Password Changed'
    PROJECT_DOCUMENTATION_DOWNLOADED = 'project_documentation_downloaded', 'Project Documentation Downloaded'
    EXTERNAL_PROJECT_COMMENT_CREATED = 'external_project_comment_created', 'External Project Comment Created'
    COMMENT_CREATED = 'comment_created', 'Comment Created'


class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=80, choices=ActivityType.choices)
    title = models.CharField(max_length=180)
    description = models.TextField()
    related_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
    )
    related_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_activities',
    )
    metadata = models.JSONField(default=dict, blank=True)
    is_seen = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_seen', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_seen', '-created_at'], name='activity_feed_idx'),
            models.Index(fields=['user', 'type', '-created_at'], name='activity_type_idx'),
            models.Index(fields=['user', 'deleted_at'], name='activity_deleted_idx'),
        ]

    def __str__(self):
        return f'{self.user_id}:{self.type}:{self.title}'

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])


class ProjectDownloadLog(models.Model):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='download_logs',
    )
    downloader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['project', 'downloaded_at'],
                name='download_log_project_date_idx'
            ),
        ]


class ProjectViewLog(models.Model):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='view_logs',
    )
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    viewed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['project', 'viewed_at'],
                name='view_log_project_date_idx'
            ),
        ]
