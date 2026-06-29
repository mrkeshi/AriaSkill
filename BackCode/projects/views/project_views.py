from django.db import IntegrityError, models, transaction
from django.db.models.functions import ExtractYear
from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.events import (project_created, project_deleted,
                             project_documentation_downloaded, project_updated)
from activity.services import ActivityService
from core.pagination import CommentPagination, ProjectPagination
from notification.services import NotificationService as NS
from projects.models import Comment, Like, Project
from projects.schemas import project_schema
from projects.serializers import (CommentManagementSerializer,
                                  DownloadCountSerializer,
                                  LikeResponseSerializer, ProjectSerializer)

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


@project_schema.project_list_create_schema
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ProjectPagination

    def get_queryset(self):
        return (
            Project.objects
            .filter(user=self.request.user)
            .select_related('user')
            .prefetch_related('skills', 'likes')
            .order_by('-created_at')
        )

    def perform_create(self, serializer):
        project = serializer.save(user=self.request.user)
        project_created.send(
            sender=project.__class__,
            user=self.request.user,
            project=project,
        )


@project_schema.project_list_all_public
class PublicProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = (
            Project.objects
            .filter(status='approved')
            .select_related('user')
            .prefetch_related('skills', 'likes')
        )

        q = self.request.query_params.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                models.Q(title__icontains=q) |
                models.Q(description__icontains=q) |
                models.Q(skills__name__icontains=q)
            ).distinct()

        technologies = self.request.query_params.getlist('technology')
        if technologies:
            queryset = queryset.filter(skills__slug__in=technologies).distinct()

        years = self.request.query_params.getlist('year')
        if years:
            try:
                year_ints = [int(y) for y in years]
                year_filters = models.Q()
                for sh_year in year_ints:
                    year_filters |= models.Q(
                        created_at__year__gte=sh_year + 621,
                        created_at__year__lte=sh_year + 622,
                    )
                queryset = queryset.filter(year_filters)
            except (ValueError, TypeError):
                pass

        categories = self.request.query_params.getlist('category')
        if categories:
            db_types = [CATEGORY_MAP.get(c, c) for c in categories]
            queryset = queryset.filter(project_type__in=db_types)

        sort = self.request.query_params.get('sort', 'new')
        if sort == 'downloads':
            queryset = queryset.annotate(
                dl_count=models.Count('download_logs')
            ).order_by('-dl_count')
        else:
            sort_map = {
                'new': '-created_at',
                'old': 'created_at',
                'popular': '-likes_count',
            }
            queryset = queryset.order_by(sort_map.get(sort, '-created_at'))

        return queryset

@project_schema.project_years_schema
class ProjectYearsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        years_qs = (
            Project.objects
            .filter(status='approved')
            .annotate(year=ExtractYear('created_at'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
        )
        shamsi_years = sorted(set(y - 621 for y in years_qs if y), reverse=True)
        return Response({'years': shamsi_years})


@project_schema.project_detail
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
        ActivityService.project_viewed(project=project, request=request)
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def ensure_owner(self, project):
        if project.user != self.request.user:
            raise PermissionDenied("You are not allowed to change this project.")

    def perform_update(self, serializer):
        project = serializer.instance
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

    @project_schema.project_like_post
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user
        try:
            with transaction.atomic():
                if Like.objects.filter(user=user, project=project).exists():
                    return Response(
                        {"detail": "You have already liked this project"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                Like.objects.create(user=user, project=project)
                Project.objects.filter(pk=project.pk).update(
                    likes_count=models.F('likes_count') + 1)
                if project.user != user:
                    NS.like_received(project_owner=project.user, project=project, liker=user)
        except IntegrityError:
            return Response(
                {"detail": "You have already liked this project"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project.refresh_from_db()
        serializer = self.get_serializer({'likes_count': project.likes_count, "liked": True})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectUnlikeView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    lookup_field = 'slug'
    serializer_class = LikeResponseSerializer

    @project_schema.project_unlike_post
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        deleted, _ = Like.objects.filter(project=project, user=request.user).delete()
        if deleted:
            Project.objects.filter(pk=project.pk).update(
                likes_count=models.F('likes_count') - 1)
            project.refresh_from_db()
            return Response({"likes_count": project.likes_count, "liked": False})
        return Response(
            {"detail": "You have not liked this project"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProjectDownloadView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    lookup_field = 'slug'
    serializer_class = DownloadCountSerializer

    @project_schema.project_download_post
    def post(self, request, *args, **kwargs):
        try:
            project = self.get_object()
        except (NotFound, Http404):
            return Response({"detail": "Not found this project"}, status=status.HTTP_404_NOT_FOUND)

        project_documentation_downloaded.send(
            sender=project.__class__,
            user=request.user,
            project=project,
            request=request,
        )
        download_count = project.download_logs.count()
        serializer = self.get_serializer({'download_count': download_count})
        return Response(serializer.data, status=status.HTTP_200_OK)


