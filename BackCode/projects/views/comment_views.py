from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from activity.events import comment_created, external_project_comment_created
from notification.services import NotificationService as NS


from django.shortcuts import get_object_or_404

from projects.serializers import CommentSerializer, CommentManagementSerializer
from projects.models import Comment, Project

from core.pagination import CommentPagination

from projects.schemas import comment_schema



@comment_schema.comment_list_create
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

@comment_schema.comment_detail_schema
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


@comment_schema.my_project_comments_schema
class MyProjectCommentsView(generics.ListAPIView):
    serializer_class = CommentManagementSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CommentPagination

    def get_queryset(self):
        return (
            Comment.objects
            .filter(project__user=self.request.user)
            .select_related('user', 'project')
            .order_by('-created_at')
        )