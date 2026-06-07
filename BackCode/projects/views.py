from django.db import transaction, IntegrityError, models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import generics, status, serializers  # اضافه شدن serializers برای خطای کامنت
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.events import (
    project_created,
    project_deleted,
    project_updated,
    project_documentation_downloaded,
    external_project_comment_created,
    comment_created,
)
from activity.services import ActivityService
from notification.services import NotificationService as NS
from core.pagination import ProjectPagination, CommentPagination
from projects.models import Project, Like, Comment
from projects.serializers import ProjectSerializer, LikeResponseSerializer, DownloadCountSerializer, CommentSerializer, \
    CommentManagementSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List User Projects",
        description="Retrieve a list of projects belonging to the authenticated user.",
        responses={200: ProjectSerializer(many=True)},
        tags=["Projects"]
    ),
    post=extend_schema(
        summary="Create New Project",
        description="Create a new project by an authenticated user. Read-only fields (e.g., likes_count) are ignored.",
        request=ProjectSerializer,
        responses={
            201: ProjectSerializer,
            400: OpenApiResponse(description="Invalid input"),
            401: OpenApiResponse(description="Authentication required")
        },
        tags=["Projects"]
    )
)
class ProjectListCreateView(generics.ListCreateAPIView):

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ProjectPagination

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).select_related('user').prefetch_related(
            'skills', 'likes'
        ).order_by('-created_at')

    def perform_create(self, serializer):
        project = serializer.save(user=self.request.user)
        project_created.send(
            sender=project.__class__,
            user=self.request.user,
            project=project,
        )


@extend_schema_view(
    get=extend_schema(
        summary="List All Projects (Public)",
        description="Retrieve a list of all projects ordered by newest first. No authentication required.",
        responses={200: ProjectSerializer(many=True)},
        tags=["Public Projects"]
    )
)
class PublicProjectListView(generics.ListAPIView):

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = Project.objects.filter(status='approved').select_related('user').prefetch_related(
            'skills', 'likes'
        )

        # جستجوی متنی
        q = self.request.query_params.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                models.Q(title__icontains=q) |
                models.Q(description__icontains=q) |
                models.Q(skills__name__icontains=q)
            ).distinct()

        # فیلتر تکنولوژی (skills)
        technologies = self.request.query_params.getlist('technology')
        if technologies:
            queryset = queryset.filter(skills__slug__in=technologies).distinct()

        # فیلتر سال (shamsi year از created_at)
        years = self.request.query_params.getlist('year')
        if years:
            try:
                year_ints = [int(y) for y in years]
                # تبدیل سال شمسی به gregorian approximate
                year_filters = models.Q()
                for sh_year in year_ints:
                    # سال شمسی به میلادی: sh_year + 621 و sh_year + 622
                    start_year = sh_year + 621
                    end_year = sh_year + 622
                    year_filters |= models.Q(
                        created_at__year__gte=start_year,
                        created_at__year__lte=end_year
                    )
                queryset = queryset.filter(year_filters)
            except (ValueError, TypeError):
                pass

        # فیلتر نوع پروژه (category)
        categories = self.request.query_params.getlist('category')
        CATEGORY_MAP = {
            'UI/UX Design': 'UI/UX',
            'Frontend Development': 'Frontend',
            'Backend Development': 'Backend',
            'Mobile Development': 'Mobile',
            'AI & Data': 'AI_Data',
            'DevOps & Cloud': 'DevOps_Cloud',
            'Game Development': 'Game',
            'Cyber Security': 'Cyber_Sec',
        }
        if categories:
            db_types = [CATEGORY_MAP.get(c, c) for c in categories]
            queryset = queryset.filter(project_type__in=db_types)

        # مرتب‌سازی
        sort = self.request.query_params.get('sort', 'new')
        sort_map = {
            'new': '-created_at',
            'old': 'created_at',
            'popular': '-likes_count',
            'downloads': '-download_count',
        }
        ordering = sort_map.get(sort, '-created_at')
        queryset = queryset.order_by(ordering)

        return queryset


class ProjectYearsView(APIView):
    """لیست سال‌های شمسی که پروژه‌ها در آن‌ها منتشر شده‌اند"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        from django.db.models.functions import ExtractYear
        years_qs = (
            Project.objects
            .filter(status='approved')
            .annotate(year=ExtractYear('created_at'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
        )
        # تبدیل به سال شمسی
        shamsi_years = sorted(set(y - 621 for y in years_qs if y), reverse=True)
        return Response({'years': shamsi_years})


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Project Details",
        description="Get detailed information about a specific project by its slug. Accessible by anyone.",
        responses={
            200: ProjectSerializer,
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    ),
    put=extend_schema(
        summary="Full Update Project",
        description="Completely replace a project. Only the owner can perform this action.",
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            400: OpenApiResponse(description="Invalid data"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="You are not allowed to update this project"),
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    ),
    patch=extend_schema(
        summary="Partial Update Project",
        description="Partially update a project. Only the owner can perform this action.",
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            400: OpenApiResponse(description="Invalid data"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="You are not allowed to update this project"),
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    ),
    delete=extend_schema(
        summary="Delete Project",
        description="Permanently delete a project. Only the owner can perform this action.",
        responses={
            204: OpenApiResponse(description="Project successfully deleted"),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="You are not allowed to delete this project"),
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    )
)
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('skills').select_related('user')
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self.request.method not in SAFE_METHODS:
            return queryset

        if user.is_authenticated and user.is_staff:
            return queryset

        if user.is_authenticated:
            return queryset.filter(models.Q(status='approved') | models.Q(user=user))

        return queryset.filter(status='approved')

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        Project.objects.filter(pk=project.pk).update(view_count=models.F('view_count') + 1)
        project.refresh_from_db(fields=['view_count'])
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def ensure_owner(self, project):
        if project.user != self.request.user:
            raise PermissionDenied("You are not allowed to change this project.")

    def perform_update(self, serializer):
        project = self.get_object()
        self.ensure_owner(project)
        updated = serializer.save()
        project_updated.send(
            sender=updated.__class__,
            user=self.request.user,
            project=updated,
        )

    def perform_destroy(self, instance):
        self.ensure_owner(instance)
        project_title = instance.title
        instance.delete()
        project_deleted.send(
            sender=instance.__class__,
            user=self.request.user,
            project_title=project_title,
        )


class ProjectLikeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    lookup_field = 'slug'
    serializer_class = LikeResponseSerializer

    @extend_schema(
        summary="Like a project",
        description="Authenticated users can like a project only once. Returns updated like count and liked status.",
        request=None,
        responses={
            201: LikeResponseSerializer,
            400: OpenApiResponse(description="Already liked or invalid project"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    )
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user
        try:
            with transaction.atomic():
                if Like.objects.filter(user=user, project=project).exists():
                    return Response({"detail": "You have already liked this project"}, status=status.HTTP_400_BAD_REQUEST)
                Like.objects.create(user=user, project=project)
                Project.objects.filter(pk=project.pk).update(likes_count=models.F('likes_count') + 1)
                if project.user != user:
                    NS.like_received(project_owner=project.user, project=project, liker=user)
        except IntegrityError:
            return Response({"detail": "You have already liked this project"}, status=status.HTTP_400_BAD_REQUEST)

        project.refresh_from_db()
        serializer = self.get_serializer({'likes_count': project.likes_count, "liked": True})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectUnlikeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    lookup_field = 'slug'
    serializer_class = LikeResponseSerializer

    @extend_schema(
        summary="Unlike a project",
        description="Remove the authenticated user's like from a project. Returns updated like count and liked=false.",
        request=None,
        responses={
            200: LikeResponseSerializer,
            400: OpenApiResponse(description="You haven't liked this project"),
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    )
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        deleted, _ = Like.objects.filter(project=project, user=request.user).delete()
        if deleted:
            Project.objects.filter(pk=project.pk).update(likes_count=models.F('likes_count') - 1)
            project.refresh_from_db()
            return Response({"likes_count": project.likes_count, "liked": False}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this project"}, status=status.HTTP_400_BAD_REQUEST)


class ProjectDownloadView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    lookup_field = 'slug'
    serializer_class = DownloadCountSerializer

    @extend_schema(
        summary="Download a project",
        description="Increment the download count of a project. Each request increases the counter by one (no duplicate prevention).",
        request=None,
        responses={
            200: DownloadCountSerializer,
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Project not found")
        },
        tags=["Projects"]
    )
    def post(self, request, *args, **kwargs):
        updated = Project.objects.filter(slug=self.kwargs['slug']).update(download_count=models.F('download_count') + 1,
                                                                          last_download=timezone.now())
        if updated == 0:
            return Response({"detail": "Not found this project"}, status=status.HTTP_404_NOT_FOUND)

        project = self.get_object()
        project_documentation_downloaded.send(
            sender=project.__class__,
            user=request.user,
            project=project,
            request=request,
        )
        serializer = self.get_serializer({'download_count': project.download_count})
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="List top-level comments",
        description="Get all comments for a project that have no parent (i.e., not replies).",
        parameters=[
            OpenApiParameter(
                name="project_id",
                location=OpenApiParameter.PATH,
                description="ID of the project",
                type=OpenApiTypes.INT,
                required=True,
            ),
        ],
        responses={
            200: CommentSerializer(many=True),
            404: OpenApiResponse(description="Project not found (if project_id invalid)"),
        },
        tags=["Comments"],
    ),
    post=extend_schema(
        summary="Create a new comment",
        description="Post a comment on a project. You can also reply to an existing comment by providing `parent` ID in request body.",
        parameters=[
            OpenApiParameter(
                name="project_id",
                location=OpenApiParameter.PATH,
                description="ID of the project",
                type=OpenApiTypes.INT,
                required=True,
            ),
        ],
        request=CommentSerializer,
        responses={
            201: CommentSerializer,
            400: OpenApiResponse(description="Validation error (e.g., parent comment not belonging to this project)"),
            404: OpenApiResponse(description="Project or parent comment not found"),
        },
        tags=["Comments"],
    ),
)
class CommentListCreateView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CommentPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Comment.objects.filter(
            project_id=project_id, parent__isnull=True, status='active'
        ).select_related('user').prefetch_related('replies')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_id'] = self.kwargs.get('project_id')
        return context

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, project)
        return Response(serializer.data, status=201)

    def perform_create(self, serializer, project):
        parent_id = self.request.data.get('parent')
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id)
            if parent.project_id != project.id:
                raise serializers.ValidationError(
                    {"parent": "نظر والد متعلق به این پروژه نیست."}
                )
        comment = serializer.save(project=project, user=self.request.user, parent=parent)

        if self.request.user != project.user:
            NS.comment_received(
                project_owner=project.user,
                project=project,
                commenter=self.request.user,
            )

        if self.request.user == project.user:
            comment_created.send(
                sender=comment.__class__,
                user=self.request.user,
                project=project,
                comment=comment,
            )
        else:
            external_project_comment_created.send(
                sender=comment.__class__,
                user=self.request.user,
                project=project,
                comment=comment,
                related_user=project.user,
            )


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve a comment",
        description="Get details of a specific comment by its primary key (ID).",
        responses={
            200: CommentSerializer,
            403: OpenApiResponse(description="Permission denied"),
            404: OpenApiResponse(description="Comment not found"),
        },
        tags=["Comments"],
    ),
    put=extend_schema(
        summary="Fully update a comment",
        description="Replace an existing comment. Only the comment owner or staff can perform this action.",
        request=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Permission denied"),
            404: OpenApiResponse(description="Comment not found"),
        },
        tags=["Comments"],
    ),
    patch=extend_schema(
        summary="Partially update a comment",
        description="Update specific fields of a comment. Only the comment owner or staff can perform this action.",
        request=CommentSerializer,
        responses={
            200: CommentSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Permission denied"),
            404: OpenApiResponse(description="Comment not found"),
        },
        tags=["Comments"],
    ),
    delete=extend_schema(
        summary="Delete a comment(owner)",
        description="Permanently delete a comment. Only the comment owner or staff can perform this action.",
        responses={
            204: OpenApiResponse(description="Comment successfully deleted (no content)"),
            403: OpenApiResponse(description="Permission denied"),
            404: OpenApiResponse(description="Comment not found"),
        },
        tags=["Comments"],
    )
)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'pk'

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user == self.request.user or self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You are not allowed to edit this comment.")

    def perform_destroy(self, instance):
        if instance.user == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You are not allowed to delete this comment.")


class MyProjectCommentsView(generics.ListAPIView):
    serializer_class = CommentManagementSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        return Comment.objects.filter(
            project__user=self.request.user
        ).select_related('user', 'project').order_by('-created_at')


class DashboardChartView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from django.db.models import Sum
        from django.db.models.functions import TruncDate
        from datetime import date, timedelta

        user = request.user

        # اگه هیچ پروژه‌ای نداره
        has_projects = Project.objects.filter(user=user).exists()
        if not has_projects:
            return Response({"days": [], "views": [], "downloads": []})

        MAX_DAYS = 20
        today = date.today()
        earliest_date = today - timedelta(days=MAX_DAYS - 1)

        from activity.models import Activity, ActivityType

        # ── Downloads per day ──────────────────────────────────────────────────
        # دانلودهایی که روی پروژه‌های این یوزر انجام شده (توسط هر کسی)
        # قبلاً: filter(user=user, ...)       ← دانلودهای خود یوزر ✗
        # الان:  filter(related_project__user=user, ...) ← دانلودهای پروژه‌هاش ✓
        from activity.models import ProjectDownloadLog

        download_qs = (
            ProjectDownloadLog.objects
            .filter(
                project__user=user,
                downloaded_at__date__gte=earliest_date,
            )
            .annotate(day=TruncDate('downloaded_at'))
            .values('day')
            .annotate(count=models.Count('id'))
            .order_by('day')
        )

        engagement_qs = (
            Activity.objects
            .filter(
                related_project__user=user,
                type__in=[
                    ActivityType.PROJECT_DOCUMENTATION_DOWNLOADED,
                    ActivityType.EXTERNAL_PROJECT_COMMENT_CREATED,
                ],
                created_at__date__gte=earliest_date,
                deleted_at__isnull=True,
            )
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(count=models.Count('id'))
            .order_by('day')
        )


        total_views = (
            Project.objects
            .filter(user=user)
            .aggregate(total=Sum('view_count'))['total'] or 0
        )


        download_by_day = {row['day']: row['count'] for row in download_qs}
        engagement_by_day = {row['day']: row['count'] for row in engagement_qs}

        all_days_with_data = set(download_by_day.keys()) | set(engagement_by_day.keys())

        if not all_days_with_data:

            return Response({
                "days": [today.isoformat()],
                "views": [total_views],
                "downloads": [0],
            })

        start_date = max(min(all_days_with_data), earliest_date)
        num_days = min((today - start_date).days + 1, MAX_DAYS)

        days = []
        views = []
        downloads = []

        for i in range(num_days):
            d = start_date + timedelta(days=i)
            days.append(d.isoformat())
            downloads.append(download_by_day.get(d, 0))

            if d == today:
                views.append(total_views)
            else:
                views.append(engagement_by_day.get(d, 0))

        return Response({
            "days": days,
            "views": views,
            "downloads": downloads,
        })
class DashboardStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from django.db.models import Sum
        from notification.models import Notification

        user = request.user
        projects_qs = Project.objects.filter(user=user)

        total_projects = projects_qs.count()
        total_downloads = projects_qs.aggregate(s=Sum('download_count'))['s'] or 0
        total_comments = Comment.objects.filter(
            project__user=user,
            status='active',
        ).count()
        unread_notifications = Notification.objects.filter(
            user=user,
            is_read=False,
            deleted_at__isnull=True,
        ).count()

        return Response({
            'total_projects':        total_projects,
            'total_downloads':       total_downloads,
            'total_comments':        total_comments,
            'unread_notifications':  unread_notifications,
        })
