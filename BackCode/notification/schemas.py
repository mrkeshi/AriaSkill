from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

UnreadCountResponse = inline_serializer(
    name="UnreadCountResponse",
    fields={"unread_count": serializers.IntegerField()},
)

MarkAllReadResponse = inline_serializer(
    name="MarkAllReadResponse",
    fields={"updated": serializers.IntegerField()},
)

BroadcastResponse = inline_serializer(
    name="BroadcastResponse",
    fields={
        "detail": serializers.CharField(),
        "count": serializers.IntegerField(),
    },
)

ClearLogsResponse = inline_serializer(
    name="ClearLogsResponse",
    fields={
        "detail": serializers.CharField(),
        "deleted": serializers.IntegerField(),
    },
)

NotFoundResponse = inline_serializer(
    name="NotFoundResponse",
    fields={"detail": serializers.CharField()},
)

notification_list_schema = extend_schema(
    summary="List user notifications",
    description=(
        "Returns a paginated list of notifications for the currently authenticated user. "
        "Results can be filtered by notification type and read status."
    ),
    parameters=[
        OpenApiParameter(
            name="type",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter by notification type. Allowed values are defined in NotificationType.",
        ),
        OpenApiParameter(
            name="is_read",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter by read status. Pass true for read, false for unread.",
        ),
    ],
    examples=[
        OpenApiExample(
            name="Filter unread notifications",
            description="Fetch all notifications that have not been read yet.",
            value={"is_read": False},
            request_only=False,
            response_only=False,
        ),
    ],
    tags=["Notifications"],
)

notification_recent_schema = extend_schema(
    summary="Get recent notifications",
    description=(
        "Returns the 10 most recent notifications for the current user without pagination. "
        "Intended for use in dropdowns or notification badges."
    ),
    tags=["Notifications"],
)

notification_unread_count_schema = extend_schema(
    summary="Get unread notification count",
    description="Returns the number of unread notifications for the currently authenticated user.",
    responses={
        200: OpenApiResponse(
            response=UnreadCountResponse,
            description="Number of unread notifications.",
            examples=[
                OpenApiExample(
                    name="Sample response",
                    value={"unread_count": 5},
                    response_only=True,
                )
            ],
        )
    },
    tags=["Notifications"],
)

notification_mark_read_schema = extend_schema(
    summary="Mark a notification as read or unread",
    description=(
        "Updates the is_read status of a specific notification. "
        "If is_read is omitted from the request body, it defaults to true."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Primary key of the notification.",
        )
    ],
    responses={
        200: OpenApiResponse(description="Notification updated successfully."),
        404: OpenApiResponse(
            response=NotFoundResponse,
            description="Notification not found or does not belong to the current user.",
            examples=[
                OpenApiExample(
                    name="Not found",
                    value={"detail": "Not found."},
                    response_only=True,
                )
            ],
        ),
    },
    examples=[
        OpenApiExample(
            name="Mark as read",
            value={"is_read": True},
            request_only=True,
        ),
        OpenApiExample(
            name="Mark as unread",
            value={"is_read": False},
            request_only=True,
        ),
    ],
    tags=["Notifications"],
)

notification_mark_all_read_schema = extend_schema(
    summary="Mark all notifications as read",
    description="Marks every unread notification belonging to the current user as read in a single operation.",
    request=None,
    responses={
        200: OpenApiResponse(
            response=MarkAllReadResponse,
            description="Number of notifications that were updated.",
            examples=[
                OpenApiExample(
                    name="Sample response",
                    value={"updated": 12},
                    response_only=True,
                )
            ],
        )
    },
    tags=["Notifications"],
)

notification_delete_schema = extend_schema(
    summary="Soft-delete a notification",
    description=(
        "Soft-deletes the specified notification by setting its deleted_at timestamp. "
        "Only Notifications that belong to the currently authenticated user can be deleted."
    ),
    parameters=[
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Primary key of the notification.",
        )
    ],
    responses={
        204: OpenApiResponse(description="Notification deleted successfully. No content returned."),
        404: OpenApiResponse(
            response=NotFoundResponse,
            description="Notification not found or does not belong to the current user.",
        ),
    },
    tags=["Notifications"],
)

admin_broadcast_schema = extend_schema(
    summary="Send a broadcast notification",
    description=(
        "Creates and dispatches a notification to all active users in the system. "
        "Accessible by admin users only."
    ),
    responses={
        201: OpenApiResponse(
            response=BroadcastResponse,
            description="Broadcast sent successfully.",
            examples=[
                OpenApiExample(
                    name="Sample response",
                    value={
                        "detail": "Broadcast successfully sent to 1248 users.",
                        "count": 1248,
                    },
                    response_only=True,
                )
            ],
        ),
        400: OpenApiResponse(description="Invalid request data."),
        403: OpenApiResponse(description="Admin access required."),
    },
    examples=[
        OpenApiExample(
            name="Sample request",
            value={
                "title": "Scheduled maintenance",
                "message": "The system will be unavailable on Friday from 2:00 to 4:00 AM.",
            },
            request_only=True,
        )
    ],
    tags=["Admin Notifications"],
)

admin_broadcast_log_list_schema = extend_schema(
    summary="List broadcast logs",
    description=(
        "Returns a paginated history of all broadcast notifications that have been sent. "
        "Accessible by admin users only."
    ),
    responses={
        200: OpenApiResponse(description="Paginated list of broadcast log entries."),
        403: OpenApiResponse(description="Admin access required."),
    },
    tags=["Admin Notifications"],
)

admin_broadcast_log_clear_schema = extend_schema(
    summary="Clear all broadcast logs",
    description=(
        "Permanently deletes all broadcast log records from the database. "
        "This action is irreversible. Accessible by admin users only."
    ),
    request=None,
    responses={
        200: OpenApiResponse(
            response=ClearLogsResponse,
            description="Number of log records that were deleted.",
            examples=[
                OpenApiExample(
                    name="Sample response",
                    value={"detail": "47 log records cleared.", "deleted": 47},
                    response_only=True,
                )
            ],
        ),
        403: OpenApiResponse(description="Admin access required."),
    },
    tags=["Admin Notifications"],
)
