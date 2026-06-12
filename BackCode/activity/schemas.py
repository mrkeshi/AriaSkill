
from drf_spectacular.utils import (OpenApiParameter, OpenApiResponse,
                                   extend_schema, extend_schema_view)

from activity.serializers import ActivitySerializer, ActivityMarkSeenSerializer



activity_recent_schema = extend_schema(
    summary="Get Recent Activities",
    description="Returns the most recent activities for the authenticated user (unpaginated).",
    tags=["Activity"],
    responses={
        200: OpenApiResponse(response=ActivitySerializer, description="Recent activities retrieved successfully"),
        401: OpenApiResponse(description="Authentication required"),
    },
)


activity_list_schema = extend_schema(
    summary="List Activities",
    description=(
        "Returns a paginated list of activities for the authenticated user.\n\n"
        "Filter by `type` and/or `is_seen` using query parameters."
    ),
    tags=["Activity"],
    parameters=[
        OpenApiParameter(
            name="type",
            description="Filter activities by type",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="is_seen",
            description="Filter by seen status (`true` or `false`)",
            required=False,
            type=bool,
        ),
    ],
    responses={
        200: OpenApiResponse(response=ActivitySerializer, description="Activities listed successfully"),
        400: OpenApiResponse(description="Invalid filter parameters"),
        401: OpenApiResponse(description="Authentication required"),
    },
)


activity_mark_seen_schema = extend_schema(
    summary="Mark Activity as Seen",
    description="Update the `is_seen` status of a specific activity owned by the authenticated user.",
    tags=["Activity"],
    request=ActivityMarkSeenSerializer,
    responses={
        200: OpenApiResponse(response=ActivitySerializer, description="Activity updated successfully"),
        400: OpenApiResponse(description="Invalid data"),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Activity not found"),
    },
)


activity_delete_schema = extend_schema(
    summary="Delete an Activity",
    description="Soft-delete a specific activity owned by the authenticated user.",
    tags=["Activity"],
    responses={
        204: OpenApiResponse(description="Activity deleted successfully"),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="Activity not found"),
    },
)


activity_unseen_count_schema = extend_schema(
    summary="Get Unseen Activity Count",
    description="Returns the count of unseen activities for the authenticated user.",
    tags=["Activity"],
    responses={
        200: OpenApiResponse(description="Unseen count returned", examples=None),
        401: OpenApiResponse(description="Authentication required"),
    },
)


activity_mark_all_seen_schema = extend_schema(
    summary="Mark All Activities as Seen",
    description="Marks all unseen activities of the authenticated user as seen. Returns the count of updated records.",
    tags=["Activity"],
    responses={
        200: OpenApiResponse(description="All activities marked as seen"),
        401: OpenApiResponse(description="Authentication required"),
    },
)