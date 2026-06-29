
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import serializers

from projects.serializers import (CommentManagementSerializer,
                                  ProjectSerializer, ProjectStatusSerializer,
                                  SkillSerializer)


class AdminProjectStatusResponseSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(
        help_text="Set to true to approve, false to reject the project"
    )


skill_list_get_schema = extend_schema(
    summary="List or Search Skills",
    tags=["Skills"],
)

skill_list_post_schema = extend_schema(
    summary="Create a new Skill",
    tags=["Skills"],
)

skill_retrieve_update_destroy_schema = extend_schema_view(
    get=extend_schema(
        summary="Retrieve a Skill",
        tags=["Skills"],
        responses={
            200: OpenApiResponse(response=SkillSerializer, description="Skill retrieved successfully"),
            404: OpenApiResponse(description="Skill not found"),
        },
    ),
    put=extend_schema(
        summary="Update a Skill",
        tags=["Skills"],
        responses={
            200: OpenApiResponse(response=SkillSerializer, description="Skill updated successfully"),
            400: OpenApiResponse(description="Invalid data"),
            403: OpenApiResponse(description="Admin access required"),
            404: OpenApiResponse(description="Skill not found"),
        },
    ),
    patch=extend_schema(
        summary="Partially Update a Skill",
        tags=["Skills"],
        responses={
            200: OpenApiResponse(response=SkillSerializer, description="Skill updated successfully"),
            400: OpenApiResponse(description="Invalid data"),
            403: OpenApiResponse(description="Admin access required"),
            404: OpenApiResponse(description="Skill not found"),
        },
    ),
    delete=extend_schema(
        summary="Delete a Skill",
        tags=["Skills"],
        responses={
            204: OpenApiResponse(description="Skill deleted successfully"),
            403: OpenApiResponse(description="Admin access required"),
            404: OpenApiResponse(description="Skill not found"),
        },
    ),
)

admin_project_list_schema = extend_schema(
    summary="Admin: List All Projects",
    description=(
        "Returns a paginated list of all projects regardless of status.\n\n"
        "Supports search by title, description, type, status, username, email, and skills."
    ),
    tags=["Admin Projects"],
    responses={
        200: OpenApiResponse(response=ProjectSerializer, description="Projects listed successfully"),
        403: OpenApiResponse(description="Admin access required"),
    },
)

admin_project_detail_schema = extend_schema(
    summary="Admin: Delete a Project",
    description="Permanently delete a project by its slug.",
    tags=["Admin Projects"],
    responses={
        204: OpenApiResponse(description="Project deleted successfully"),
        403: OpenApiResponse(description="Admin access required"),
        404: OpenApiResponse(description="Project not found"),
    },
)

admin_project_status_schema = extend_schema(
    summary="Admin: Approve or Reject a Project",
    description=(
        "Update the status of a project.\n\n"
        "- `is_active: true` → status becomes **approved**\n"
        "- `is_active: false` → status becomes **rejected**\n\n"
        "A `project_published` signal is fired when a project is approved for the first time."
    ),
    tags=["Admin Projects"],
    request=ProjectStatusSerializer,
    responses={
        200: OpenApiResponse(
            response=ProjectSerializer,
            description="Project status updated successfully",
            examples=[
                OpenApiExample(
                    name="Approve project",
                    value={"is_active": True},
                    request_only=True,
                ),
                OpenApiExample(
                    name="Reject project",
                    value={"is_active": False},
                    request_only=True,
                ),
            ],
        ),
        400: OpenApiResponse(description="Invalid data"),
        403: OpenApiResponse(description="Admin access required"),
        404: OpenApiResponse(description="Project not found"),
    },
)

admin_comment_list_schema = extend_schema_view(
    get=extend_schema(
        summary="Admin: List All Comments",
        description=(
            "Paginated list of all comments across all projects.\n\n"
            "Supports search by message, username, email, and project title.\n"
            "Filter by status using `?status=active` or `?status=inactive`."
        ),
        tags=["Admin Comments"],
        parameters=[
            OpenApiParameter(
                name='status',
                description="Filter comments by status",
                required=False,
                type=str,
                enum=['active', 'inactive'],
            ),
        ],
        responses={
            200: OpenApiResponse(response=CommentManagementSerializer, description="Comments listed successfully"),
            403: OpenApiResponse(description="Admin access required"),
        },
    )
)

admin_comment_moderation_schema = extend_schema_view(
    patch=extend_schema(
        summary="Admin: Toggle Comment Status",
        description="Set comment status to `active` or `inactive`.",
        tags=["Admin Comments"],
        responses={
            200: OpenApiResponse(response=CommentManagementSerializer, description="Comment status updated"),
            400: OpenApiResponse(description="Invalid status value"),
            403: OpenApiResponse(description="Admin access required"),
            404: OpenApiResponse(description="Comment not found"),
        },
    ),
    delete=extend_schema(
        summary="Admin: Delete Comment",
        description="Permanently delete a comment by its ID.",
        tags=["Admin Comments"],
        responses={
            204: OpenApiResponse(description="Comment deleted successfully"),
            403: OpenApiResponse(description="Admin access required"),
            404: OpenApiResponse(description="Comment not found"),
        },
    ),
)
