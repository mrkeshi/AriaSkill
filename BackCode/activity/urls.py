from django.urls import path

from activity.views import (
    ActivityRecentView,
    ActivityListView,
    ActivityMarkSeenView,
    ActivityDeleteView,
    ActivityUnseenCountView,
    ActivityMarkAllSeenView,
)

urlpatterns = [
    path('recent/', ActivityRecentView.as_view(), name='activity-recent'),
    path('unseen-count/', ActivityUnseenCountView.as_view(), name='activity-unseen-count'),
    path('mark-all-seen/', ActivityMarkAllSeenView.as_view(), name='activity-mark-all-seen'),
    path('', ActivityListView.as_view(), name='activity-list'),
    path('<int:pk>/mark-seen/', ActivityMarkSeenView.as_view(), name='activity-mark-seen'),
    path('<int:pk>/', ActivityDeleteView.as_view(), name='activity-delete'),
]
