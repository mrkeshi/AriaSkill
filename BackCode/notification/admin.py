from django.contrib import admin

from notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'type', 'title', 'is_read', 'created_at')
    list_filter   = ('type', 'is_read')
    search_fields = ('user__username', 'user__email', 'title', 'message')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
