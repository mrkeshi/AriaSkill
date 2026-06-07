from django.urls import path

from notification.views import (
    AdminBroadcastView,
    NotificationDeleteView,
    NotificationListView,
    NotificationMarkAllReadView,
    NotificationMarkReadView,
    NotificationRecentView,
    NotificationUnreadCountView,
)

urlpatterns = [
    path('recent/',           NotificationRecentView.as_view(),      name='notification-recent'),
    path('unread-count/',     NotificationUnreadCountView.as_view(),  name='notification-unread-count'),
    path('mark-all-read/',    NotificationMarkAllReadView.as_view(),  name='notification-mark-all-read'),
    path('admin/broadcast/',  AdminBroadcastView.as_view(),           name='notification-broadcast'),
    path('',                  NotificationListView.as_view(),         name='notification-list'),
    path('<int:pk>/mark-read/', NotificationMarkReadView.as_view(),   name='notification-mark-read'),
    path('<int:pk>/',           NotificationDeleteView.as_view(),      name='notification-delete'),
]
