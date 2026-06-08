from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from notification.models import BroadcastLog, Notification, NotificationType

User = get_user_model()

class NotificationService:

    @staticmethod
    def create(
        *,
        user,
        type: str,
        title: str,
        message: str,
        related_project=None,
        related_user=None,
        metadata: dict[str, Any] | None = None,
    ) -> Notification | None:
        if not user:
            return None
        return Notification.objects.create(
            user=user,
            type=type,
            title=title,
            message=message,
            related_project=related_project,
            related_user=related_user,
            metadata=metadata or {},
        )

    @staticmethod
    def feed_for(user) -> QuerySet:
        return (
            Notification.objects
            .filter(user=user, deleted_at__isnull=True)
            .select_related('related_project', 'related_user')
            .order_by('is_read', '-created_at')
        )

    @staticmethod
    def recent_for(user, limit: int = 6) -> QuerySet:
        return NotificationService.feed_for(user)[:limit]

    @staticmethod
    def unread_count(user) -> int:
        return NotificationService.feed_for(user).filter(is_read=False).count()

    @staticmethod
    def mark_read(notification: Notification, is_read: bool = True) -> Notification:
        notification.is_read = is_read
        notification.save(update_fields=['is_read', 'updated_at'])
        return notification

    @staticmethod
    def mark_all_read(user) -> int:
        return (
            NotificationService.feed_for(user)
            .filter(is_read=False)
            .update(is_read=True)
        )

    @staticmethod
    def delete(notification: Notification) -> None:
        notification.soft_delete()

    @staticmethod
    def login_failed(user, request=None, identifier: str = '') -> Notification | None:

        ip = ''
        if request:
            forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
            ip = forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR', '')

        msg = 'یک تلاش ناموفق برای ورود به حساب کاربری شما ثبت شد.'
        if ip:
            msg += f' آی‌پی: {ip}'

        return NotificationService.create(
            user=user,
            type=NotificationType.LOGIN_FAILED,
            title='تلاش ورود ناموفق',
            message=msg,
            metadata={'ip': ip, 'identifier': identifier},
        )

    @staticmethod
    def comment_received(project_owner, project, commenter) -> Notification | None:
        
        commenter_name = (
            f'{commenter.first_name} {commenter.last_name}'.strip()
            or commenter.username
        )
        return NotificationService.create(
            user=project_owner,
            type=NotificationType.COMMENT_CREATED,
            title='نظر جدید در پروژه‌ی شما',
            message=f'«{commenter_name}» برای پروژه «{project.title}» نظر جدیدی ثبت کرد.',
            related_project=project,
            related_user=commenter,
            metadata={'project_slug': project.slug, 'commenter_id': commenter.id},
        )

    @staticmethod
    def like_received(project_owner, project, liker) -> Notification | None:
        
        liker_name = (
            f'{liker.first_name} {liker.last_name}'.strip()
            or liker.username
        )
        return NotificationService.create(
            user=project_owner,
            type=NotificationType.LIKE_RECEIVED,
            title='لایک جدید در پروژه‌ی شما',
            message=f'«{liker_name}» پروژه «{project.title}» شما را پسندید.',
            related_project=project,
            related_user=liker,
            metadata={'project_slug': project.slug, 'liker_id': liker.id},
        )

    @staticmethod
    def broadcast(admin_user, message: str, title: str = 'پیام همگانی') -> int:
        
        users = User.objects.filter(is_active=True)
        notifications = [
            Notification(
                user=u,
                type=NotificationType.BROADCAST,
                title=title,
                message=message,
                related_user=admin_user,
                metadata={'sent_by': admin_user.id},
            )
            for u in users
        ]
        created = Notification.objects.bulk_create(notifications)
        count = len(created)
        BroadcastLog.objects.create(
            sent_by=admin_user,
            title=title,
            message=message,
            sent_to_count=count,
        )

        return count

class BroadcastLogService:

    @staticmethod
    def list_logs(page: int = 1, page_size: int = 8):
        
        return (
            BroadcastLog.objects
            .select_related('sent_by')
            .order_by('-sent_at')
        )

    @staticmethod
    def clear_all() -> int:
        
        count, _ = BroadcastLog.objects.all().delete()
        return count
