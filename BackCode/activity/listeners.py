from django.dispatch import receiver

from activity.events import (
    comment_created,
    external_project_comment_created,
    password_changed,
    project_created,
    project_deleted,
    project_documentation_downloaded,
    project_published,
    project_updated,
)
from activity.services import ActivityService


@receiver(password_changed)
def log_password_changed(sender, user, request=None, related_user=None, method='account', **kwargs):
    ActivityService.password_changed(user, request=request, related_user=related_user, method=method)


@receiver(project_published)
def log_project_published(sender, project, **kwargs):
    ActivityService.project_published(project.user, project)


@receiver(project_created)
def log_project_created(sender, user, project, **kwargs):
    ActivityService.project_created(user, project)


@receiver(project_updated)
def log_project_updated(sender, user, project, **kwargs):
    ActivityService.project_updated(user, project)


@receiver(project_deleted)
def log_project_deleted(sender, user, project_title, **kwargs):
    ActivityService.project_deleted(user, project_title)


@receiver(project_documentation_downloaded)
def log_project_documentation_downloaded(sender, user, project, request=None, **kwargs):
    ActivityService.project_documentation_downloaded(user, project, request=request)


@receiver(external_project_comment_created)
def log_external_project_comment_created(sender, user, project, comment, related_user=None, **kwargs):
    ActivityService.external_project_comment_created(user, project, comment, related_user=related_user)


@receiver(comment_created)
def log_comment_created(sender, user, project, comment, **kwargs):
    ActivityService.comment_created(user, project, comment)
