from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view, OpenApiExample)
from rest_framework import serializers
from projects.serializers import ProjectSerializer, LikeResponseSerializer, DownloadCountSerializer

class ProjectYearsSerializer(serializers.Serializer):
    years = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of Shamsi (Solar Hijri) years that have approved projects (e.g. [1403, 1402])"
    )

project_list_create_schema = extend_schema_view(
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

project_list_all_public = extend_schema_view(
    get=extend_schema(
        summary="List All Projects (Public)",
        description="Retrieve a list of all projects ordered by newest first. No authentication required.",
        responses={200: ProjectSerializer(many=True)},
        tags=["Public Projects"]
    )
)

project_detail = extend_schema_view(
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

project_like_post = extend_schema(
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

project_unlike_post = extend_schema(
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

project_download_post = extend_schema(
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


project_years_schema = extend_schema(
    summary="List available project years",
    description=(
        "Returns a list of distinct Shamsi (Solar Hijri) years in which approved projects exist.\n\n"
        "- Years are sorted in descending order.\n"
        "- Converted from Gregorian by subtracting 621."
    ),
    tags=["Projects"],
    responses={
        200: OpenApiResponse(
            response=ProjectYearsSerializer,
            description="Years retrieved successfully",
            examples=[
                OpenApiExample(
                    name="Sample response",
                    value={"years": [1403, 1402, 1401]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="No approved projects",
                    value={"years": []},
                    response_only=True,
                ),
            ],
        ),
    },
)