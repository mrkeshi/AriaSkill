from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import serializers


class DashboardChartSerializer(serializers.Serializer):
    days = serializers.ListField(
        child=serializers.DateField(),
        help_text="List of dates in ISO format (e.g. 2024-01-01)"
    )
    views = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        help_text="Number of views per day"
    )
    downloads = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        help_text="Number of downloads per day"
    )


class DashboardStatsSerializer(serializers.Serializer):
    total_projects = serializers.IntegerField(
        min_value=0,
        help_text="Total number of user's projects"
    )
    total_downloads = serializers.IntegerField(
        min_value=0,
        help_text="Total number of downloads across all projects"
    )
    total_comments = serializers.IntegerField(
        min_value=0,
        help_text="Total number of active comments on user's projects"
    )
    unread_notifications = serializers.IntegerField(
        min_value=0,
        help_text="Number of unread notifications"
    )



dashboard_chart_schema = extend_schema(
    tags=["Dashboard"],
    summary="Daily views and downloads chart for the last 20 days",
    description=(
        "Returns daily view and download statistics for the authenticated user's projects "
        "over the past 20 days.\n\n"
        "- If the user has no projects, empty arrays are returned.\n"
        "- Dates are returned in ISO format (Gregorian calendar).\n"
        "- All 20 days are included even if there were no views or downloads on that day."
    ),
    responses={
        200: OpenApiResponse(
            response=DashboardChartSerializer,
            description="Daily statistics retrieved successfully",
            examples=[
                OpenApiExample(
                    name="User with projects",
                    value={
                        "days": ["2024-01-01", "2024-01-02", "2024-01-03"],
                        "views": [5, 12, 3],
                        "downloads": [1, 4, 0],
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="User with no projects",
                    value={
                        "days": [],
                        "views": [],
                        "downloads": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        401: OpenApiResponse(description="Authentication credentials were not provided"),
    },
)


dashboard_stats_schema = extend_schema(
    tags=["Dashboard"],
    summary="Overview statistics for the authenticated user's dashboard",
    description=(
        "Returns a summary of the authenticated user's dashboard stats:\n\n"
        "- **total_projects**: Total number of projects created by the user\n"
        "- **total_downloads**: Total number of downloads across all projects\n"
        "- **total_comments**: Total number of active comments on user's projects\n"
        "- **unread_notifications**: Number of unread notifications"
    ),
    responses={
        200: OpenApiResponse(
            response=DashboardStatsSerializer,
            description="Dashboard statistics retrieved successfully",
            examples=[
                OpenApiExample(
                    name="Active user",
                    value={
                        "total_projects": 12,
                        "total_downloads": 340,
                        "total_comments": 27,
                        "unread_notifications": 5,
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="New user",
                    value={
                        "total_projects": 0,
                        "total_downloads": 0,
                        "total_comments": 0,
                        "unread_notifications": 0,
                    },
                    response_only=True,
                ),
            ],
        ),
        401: OpenApiResponse(description="Authentication credentials were not provided"),
    },
)