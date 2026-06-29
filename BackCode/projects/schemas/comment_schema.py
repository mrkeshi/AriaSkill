from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view, OpenApiParameter, OpenApiExample)

from projects.serializers import CommentSerializer, CommentManagementSerializer

comment_list_create = extend_schema_view(
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

comment_detail_schema = extend_schema_view(
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

my_project_comments_schema = extend_schema(
    summary="List comments on my projects",
    description=(
        "Returns a paginated list of all comments left on the authenticated user's projects.\n\n"
        "- Sorted by most recent first.\n"
        "- Only comments belonging to projects owned by the current user are returned."
    ),
    tags=["Comments"],
    responses={
        200: OpenApiResponse(
            response=CommentManagementSerializer,
            description="Comments retrieved successfully",
            examples=[
                OpenApiExample(
                    name="Sample response",
                    value={
                        "count": 2,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "user": "john_doe",
                                "message": "Great project!",
                                "status": "active",
                                "created_at": "2024-01-15T10:30:00Z",
                                "project_title": "My Awesome Project",
                                "project_slug": "my-awesome-project",
                            },
                            {
                                "id": 2,
                                "user": "jane_doe",
                                "message": "Really helpful, thanks!",
                                "status": "active",
                                "created_at": "2024-01-14T08:00:00Z",
                                "project_title": "My Awesome Project",
                                "project_slug": "my-awesome-project",
                            },
                        ],
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="No comments yet",
                    value={
                        "count": 0,
                        "next": None,
                        "previous": None,
                        "results": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        401: OpenApiResponse(description="Authentication credentials were not provided"),
    },
)
