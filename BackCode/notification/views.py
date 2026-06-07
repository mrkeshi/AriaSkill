from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import Notification
from notification.serializers import (
    BroadcastSerializer,
    NotificationFilterSerializer,
    NotificationMarkReadSerializer,
    NotificationSerializer,
)
from notification.services import NotificationService


class NotificationListView(generics.ListAPIView):
    """GET /api/notifications/ — full paginated list with optional filters."""
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        filter_ser = NotificationFilterSerializer(data=self.request.query_params)
        filter_ser.is_valid(raise_exception=True)
        filters = filter_ser.validated_data

        qs = NotificationService.feed_for(self.request.user)

        if 'type' in filters:
            qs = qs.filter(type=filters['type'])
        if 'is_read' in filters:
            qs = qs.filter(is_read=filters['is_read'])

        return qs


class NotificationRecentView(APIView):
    """GET /api/notifications/recent/ — latest 6, unread first."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        items = NotificationService.recent_for(request.user)
        return Response(NotificationSerializer(items, many=True).data)


class NotificationUnreadCountView(APIView):
    """GET /api/notifications/unread-count/"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'unread_count': NotificationService.unread_count(request.user)})


class NotificationMarkReadView(APIView):
    """PATCH /api/notifications/<id>/mark-read/"""
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        notif = self._get_owned(pk, request.user)
        if notif is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        ser = NotificationMarkReadSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        updated = NotificationService.mark_read(notif, ser.validated_data['is_read'])
        return Response(NotificationSerializer(updated).data)

    @staticmethod
    def _get_owned(pk, user):
        return Notification.objects.filter(
            pk=pk, user=user, deleted_at__isnull=True
        ).first()


class NotificationMarkAllReadView(APIView):
    """PATCH /api/notifications/mark-all-read/"""
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        updated = NotificationService.mark_all_read(request.user)
        return Response({'updated': updated})


class NotificationDeleteView(APIView):
    """DELETE /api/notifications/<id>/"""
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        notif = Notification.objects.filter(
            pk=pk, user=request.user, deleted_at__isnull=True
        ).first()
        if notif is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        NotificationService.delete(notif)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin-only ─────────────────────────────────────────────────────────────────

class AdminBroadcastView(APIView):
    """
    POST /api/notifications/admin/broadcast/
    Admin sends a broadcast message to ALL active users.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request):
        ser = BroadcastSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        count = NotificationService.broadcast(
            admin_user=request.user,
            title=ser.validated_data['title'],
            message=ser.validated_data['message'],
        )
        return Response(
            {'detail': f'پیام همگانی با موفقیت برای {count} کاربر ارسال شد.', 'count': count},
            status=status.HTTP_201_CREATED,
        )
