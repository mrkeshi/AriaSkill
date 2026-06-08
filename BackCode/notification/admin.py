from django.contrib import admin

from notification.models import BroadcastLog, Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display    = ('id', 'user', 'type', 'title', 'is_read', 'created_at')
    list_filter     = ('type', 'is_read')
    search_fields   = ('user__username', 'user__email', 'title', 'message')
    ordering        = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(BroadcastLog)
class BroadcastLogAdmin(admin.ModelAdmin):
    list_display    = ('id', 'sent_by', 'title', 'sent_to_count', 'sent_at')
    search_fields   = ('title', 'message', 'sent_by__username')
    ordering        = ('-sent_at',)
    readonly_fields = ('sent_by', 'title', 'message', 'sent_to_count', 'sent_at')

    def has_add_permission(self, request):
        return False  

    def has_change_permission(self, request, obj=None):
        return False
