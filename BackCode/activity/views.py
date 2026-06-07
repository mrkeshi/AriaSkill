from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.models import Activity
from activity.serializers import ActivitySerializer, ActivityMarkSeenSerializer, ActivityFilterSerializer
from activity.services import ActivityService
from core.pagination import ActivityPagination


class ActivityRecentView(APIView):
    """GET /api/activities/recent/ — latest 6 activities, unseen first."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        activities = ActivityService.recent_for(request.user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ActivityListView(generics.ListAPIView):
    """GET /api/activities/ — full paginated feed with optional filters."""
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerializer
    pagination_class = ActivityPagination

    def get_queryset(self):
        filter_serializer = ActivityFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        qs = ActivityService.feed_for(self.request.user)

        if 'type' in filters:
            qs = qs.filter(type=filters['type'])

        if 'is_seen' in filters:
            qs = qs.filter(is_seen=filters['is_seen'])

        return qs


class ActivityMarkSeenView(APIView):
    """PATCH /api/activities/<id>/mark-seen/"""
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        activity = self._get_owned(pk, request.user)
        if activity is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActivityMarkSeenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated = ActivityService.mark_seen(activity, serializer.validated_data['is_seen'])
        return Response(ActivitySerializer(updated).data)

    @staticmethod
    def _get_owned(pk, user):
        return Activity.objects.filter(pk=pk, user=user, deleted_at__isnull=True).first()


class ActivityDeleteView(APIView):
    """DELETE /api/activities/<id>/"""
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        activity = Activity.objects.filter(pk=pk, user=request.user, deleted_at__isnull=True).first()
        if activity is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        ActivityService.delete(activity)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityUnseenCountView(APIView):
    """GET /api/activities/unseen-count/"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        count = ActivityService.feed_for(request.user).filter(is_seen=False).count()
        return Response({'unseen_count': count})


class ActivityMarkAllSeenView(APIView):
    """PATCH /api/activities/mark-all-seen/"""
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        updated = ActivityService.feed_for(request.user).filter(is_seen=False).update(is_seen=True)
        return Response({'updated': updated})
