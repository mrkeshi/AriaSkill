from typing import Any

from django.db.models import QuerySet
from django.utils import timezone

from activity.models import Activity, ActivityType


def request_metadata(request) -> dict[str, Any]:
    if not request:
        return {}
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    ip_address = forwarded_for.split(',')[0].strip() if forwarded_for else request.META.get('REMOTE_ADDR', '')
    return {
        'ip_address': ip_address,
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
    }


class ActivityService:

    @staticmethod
    def create(
        *,
        user,
        type: str,
        title: str,
        description: str,
        related_project=None,
        related_user=None,
        metadata: dict[str, Any] | None = None,
    ) -> Activity | None:
        if not user or not getattr(user, 'is_authenticated', False):
            return None
        return Activity.objects.create(
            user=user,
            type=type,
            title=title,
            description=description,
            related_project=related_project,
            related_user=related_user,
            metadata=metadata or {},
        )

    @staticmethod
    def feed_for(user) -> QuerySet:
        return (
            Activity.objects
            .filter(user=user, deleted_at__isnull=True)
            .select_related('related_project', 'related_user')
            .order_by('is_seen', '-created_at')
        )

    @staticmethod
    def recent_for(user, limit: int = 6) -> QuerySet:
        return ActivityService.feed_for(user)[:limit]

    @staticmethod
    def mark_seen(activity: Activity, is_seen: bool = True) -> Activity:
        activity.is_seen = is_seen
        activity.save(update_fields=['is_seen', 'updated_at'])
        return activity

    @staticmethod
    def delete(activity: Activity) -> None:
        activity.soft_delete()

    # ── Auth ──────────────────────────────────────────────────────────────────

    @staticmethod
    def login_success(user, request=None, method: str = 'password') -> Activity | None:
        meta = request_metadata(request)
        meta['method'] = method
        ip = meta.get('ip_address', '')
        method_label = 'گوگل' if method == 'google' else 'رمز عبور'
        desc = f'ورود موفق از طریق {method_label}'
        if ip:
            desc += f' — آی‌پی: {ip}'
        return ActivityService.create(
            user=user,
            type=ActivityType.LOGIN_SUCCESS,
            title='ورود موفق',
            description=desc,
            metadata=meta,
        )

    @staticmethod
    def login_failed(user, request=None, identifier: str = '') -> Activity | None:
        meta = request_metadata(request)
        meta['identifier'] = identifier
        ip = meta.get('ip_address', '')
        desc = 'تلاش ناموفق برای ورود'
        if ip:
            desc += f' — آی‌پی: {ip}'
        return ActivityService.create(
            user=user,
            type=ActivityType.LOGIN_FAILED,
            title='تلاش ورود ناموفق',
            description=desc,
            metadata=meta,
        )

    @staticmethod
    def password_changed(user, request=None, related_user=None, method: str = 'account') -> Activity | None:
        meta = request_metadata(request)
        meta['method'] = method
        labels = {
            'account': 'از طریق پروفایل',
            'reset': 'از طریق بازیابی رمز',
            'admin': 'توسط مدیر سیستم',
        }
        return ActivityService.create(
            user=user,
            type=ActivityType.PASSWORD_CHANGED,
            title='تغییر رمز عبور',
            description=f'رمز عبور {labels.get(method, method)} تغییر کرد.',
            related_user=related_user if related_user and related_user != user else None,
            metadata=meta,
        )

    # ── Projects ──────────────────────────────────────────────────────────────

    @staticmethod
    def project_published(user, project) -> Activity | None:
        return ActivityService.create(
            user=user,
            type=ActivityType.PROJECT_PUBLISHED,
            title='انتشار پروژه',
            description=f'پروژه «{project.title}» منتشر شد.',
            related_project=project,
            metadata={'project_slug': project.slug},
        )

    @staticmethod
    def project_created(user, project) -> Activity | None:
        return ActivityService.create(
            user=user,
            type=ActivityType.PROJECT_CREATED,
            title='ایجاد پروژه جدید',
            description=f'پروژه «{project.title}» ایجاد شد.',
            related_project=project,
            metadata={'project_slug': project.slug},
        )

    @staticmethod
    def project_updated(user, project) -> Activity | None:
        return ActivityService.create(
            user=user,
            type=ActivityType.PROJECT_UPDATED,
            title='ویرایش پروژه',
            description=f'پروژه «{project.title}» ویرایش شد.',
            related_project=project,
            metadata={'project_slug': project.slug},
        )

    @staticmethod
    def project_deleted(user, project_title: str) -> Activity | None:
        return ActivityService.create(
            user=user,
            type=ActivityType.PROJECT_DELETED,
            title='حذف پروژه',
            description=f'پروژه «{project_title}» حذف شد.',
            metadata={'project_title': project_title},
        )

    @staticmethod
    def project_documentation_downloaded(user, project, request=None) -> Activity | None:
        meta = request_metadata(request)
        meta['project_slug'] = project.slug

        from activity.models import ProjectDownloadLog
        ProjectDownloadLog.objects.create(
            project=project,
            downloader=user if getattr(user, 'is_authenticated', False) else None,
            ip_address=meta.get('ip_address'),
        )

        return ActivityService.create(
            user=user,
            type=ActivityType.PROJECT_DOCUMENTATION_DOWNLOADED,
            title='دانلود مستندات پروژه',
            description=f'فایل پروژه «{project.title}» دانلود شد.',
            related_project=project,
            metadata=meta,
        )

    # ── Comments ──────────────────────────────────────────────────────────────

    @staticmethod
    def comment_created(user, project, comment) -> Activity | None:
        return ActivityService.create(
            user=user,
            type=ActivityType.COMMENT_CREATED,
            title='ثبت دیدگاه',
            description=f'برای پروژه «{project.title}» دیدگاه ثبت کردید.',
            related_project=project,
            metadata={'comment_id': comment.id, 'project_slug': project.slug},
        )

    @staticmethod
    def external_project_comment_created(user, project, comment, related_user=None) -> Activity | None:
        return ActivityService.create(
            user=user,
            type=ActivityType.EXTERNAL_PROJECT_COMMENT_CREATED,
            title='ثبت دیدگاه در پروژه دیگران',
            description=f'برای پروژه «{project.title}» دیدگاه ثبت کردید.',
            related_project=project,
            related_user=related_user,
            metadata={'comment_id': comment.id, 'project_slug': project.slug},
        )