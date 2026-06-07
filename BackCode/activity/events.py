from django.dispatch import Signal

password_changed = Signal()
project_published = Signal()
project_created = Signal()
project_updated = Signal()
project_deleted = Signal()
project_documentation_downloaded = Signal()
external_project_comment_created = Signal()
comment_created = Signal()
