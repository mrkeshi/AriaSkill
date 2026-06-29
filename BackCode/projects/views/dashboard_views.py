from datetime import timedelta

from activity.models import ProjectDownloadLog, ProjectViewLog
from django.db import models
from django.db.models.functions import TruncDate
from django.utils import timezone
from notification.models import Notification
from projects.models import Comment, Project
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.schemas.dashboard_schema import dashboard_chart_schema, dashboard_stats_schema


@dashboard_chart_schema
class DashboardChartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        if not Project.objects.filter(user=user).exists():
            return Response({"days": [], "views": [], "downloads": []})

        MAX_DAYS = 20
        today = timezone.localdate()
        earliest_date = today - timedelta(days=MAX_DAYS - 1)

        download_qs = (
            ProjectDownloadLog.objects
            .filter(project__user=user, downloaded_at__date__gte=earliest_date)
            .annotate(day=TruncDate('downloaded_at'))
            .values('day')
            .annotate(count=models.Count('id'))
            .order_by('day')
        )

        view_qs = (
            ProjectViewLog.objects
            .filter(project__user=user, viewed_at__date__gte=earliest_date)
            .annotate(day=TruncDate('viewed_at'))
            .values('day')
            .annotate(count=models.Count('id'))
            .order_by('day')
        )

        download_by_day = {row['day']: row['count'] for row in download_qs}
        view_by_day = {row['day']: row['count'] for row in view_qs}

        days, views, downloads = [], [], []
        for i in range(MAX_DAYS):
            d = earliest_date + timedelta(days=i)
            days.append(d.isoformat())
            views.append(view_by_day.get(d, 0))
            downloads.append(download_by_day.get(d, 0))

        return Response({"days": days, "views": views, "downloads": downloads})

@dashboard_stats_schema
class DashboardStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        total_projects = Project.objects.filter(user=user).count()
        total_downloads = ProjectDownloadLog.objects.filter(project__user=user).count()
        total_comments = Comment.objects.filter(project__user=user, status='active').count()
        unread_notifications = Notification.objects.filter(
            user=user,
            is_read=False,
            deleted_at__isnull=True,
        ).count()

        return Response({
            'total_projects': total_projects,
            'total_downloads': total_downloads,
            'total_comments': total_comments,
            'unread_notifications': unread_notifications,
        })