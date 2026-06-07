from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import Skill, Project, Comment
from .serializers import SkillSerializer, ProjectSerializer, ProjectStatusSerializer, CommentManagementSerializer
from activity.events import project_published as project_published_signal
from core.pagination import ProjectPagination, CommentPagination
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by('-id')
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    @extend_schema(summary="List or Search Skills", tags=["Skills"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Create a new Skill", tags=["Skills"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(summary="Retrieve a skill", tags=["Skills"]),
    put=extend_schema(summary="Update a skill (Admin)", tags=["Skills"]),
    patch=extend_schema(summary="Partial update a skill (Admin)", tags=["Skills"]),
    delete=extend_schema(summary="Delete a skill (Admin)", tags=["Skills"]),
)
class SkillRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


@extend_schema_view(
    get=extend_schema(summary="Admin: List All Projects", tags=["Admin Projects"])
)
class AdminProjectListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'description', 'project_type', 'status',
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'skills__name',
    ]

    def get_queryset(self):
        return Project.objects.all().select_related('user').prefetch_related(
            'skills', 'likes', 'comments'
        ).order_by('-created_at')


class AdminProjectDetailView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Project.objects.all().select_related('user').prefetch_related('skills')


class AdminProjectStatusView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ProjectStatusSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Project.objects.all().select_related('user').prefetch_related('skills')

    def patch(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = 'approved' if serializer.validated_data['is_active'] else 'rejected'
        was_approved_before = project.status == 'approved'
        project.status = new_status
        project.save(update_fields=['status', 'updated_at'])

        if new_status == 'approved' and not was_approved_before:
            project_published_signal.send(sender=project.__class__, project=project)

        return Response(ProjectSerializer(project, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="Admin: List All Comments",
        description="Paginated list of all comments across all projects. Supports search by message, username, project title.",
        tags=["Admin Comments"],
    )
)
class AdminCommentListView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CommentManagementSerializer
    pagination_class = CommentPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'message',
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'project__title',
    ]

    def get_queryset(self):
        qs = Comment.objects.select_related('user', 'project').order_by('-created_at')
        status_filter = self.request.query_params.get('status')
        if status_filter in ('active', 'inactive'):
            qs = qs.filter(status=status_filter)
        return qs


@extend_schema_view(
    patch=extend_schema(
        summary="Admin: Toggle Comment Status",
        description="Set comment status to active or inactive.",
        tags=["Admin Comments"],
        responses={200: CommentManagementSerializer},
    ),
    delete=extend_schema(
        summary="Admin: Delete Comment",
        description="Permanently delete a comment.",
        tags=["Admin Comments"],
        responses={204: OpenApiResponse(description="Deleted")},
    ),
)
class AdminCommentModerationView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CommentManagementSerializer
    queryset = Comment.objects.select_related('project', 'user')
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        comment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ('active', 'inactive'):
            return Response(
                {'status': 'مقدار status باید active یا inactive باشد.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        comment.status = new_status
        comment.save(update_fields=['status', 'updated_at'])
        return Response(self.get_serializer(comment).data)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
