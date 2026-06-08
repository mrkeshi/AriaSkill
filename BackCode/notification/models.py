from django.conf import settings
from django.db import models
from django.utils import timezone

class NotificationType(models.TextChoices):
    LOGIN_FAILED     = 'login_failed',     'Login Failed'
    COMMENT_CREATED  = 'comment_created',  'Comment Created'
    LIKE_RECEIVED    = 'like_received',    'Like Received'
    BROADCAST        = 'broadcast',        'Broadcast (Admin)'

class Notification(models.Model):
    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='Recipient of the notification.',
    )
    type = models.CharField(max_length=30, choices=NotificationType.choices)
    title = models.CharField(max_length=180)
    message = models.TextField()
    related_project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
    )
    related_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
    )
    metadata = models.JSONField(default=dict, blank=True)

    is_read = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_read', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at'], name='notif_feed_idx'),
            models.Index(fields=['user', 'type', '-created_at'],    name='notif_type_idx'),
            models.Index(fields=['user', 'deleted_at'],             name='notif_deleted_idx'),
        ]

    def __str__(self):
        return f'[{self.type}] {self.user_id}: {self.title}'

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

class BroadcastLog(models.Model):
    
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='broadcast_logs',
        help_text='Admin who sent the broadcast.',
    )
    title       = models.CharField(max_length=180)
    message     = models.TextField()
    sent_to_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of users who received this broadcast.',
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['-sent_at'], name='broadcastlog_sent_at_idx'),
        ]

    def __str__(self):
        sender = self.sent_by.username if self.sent_by else 'deleted-admin'
        return f'[Broadcast] {sender}: {self.title} — {self.sent_to_count} users @ {self.sent_at:%Y-%m-%d %H:%M}'
