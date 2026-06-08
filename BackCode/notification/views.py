from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import Notification
from notification.serializers import (
    BroadcastLogSerializer,
    BroadcastSerializer,
    NotificationFilterSerializer,
    NotificationMarkReadSerializer,
    NotificationSerializer,
)
from notification.services import BroadcastLogService, NotificationService

class StandardPagination(PageNumberPagination):
    page_size            = 8
    page_size_query_param = 'page_size'
    max_page_size        = 50

class NotificationListView(generics.ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class   = NotificationSerializer

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
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        items = NotificationService.recent_for(request.user)
        return Response(NotificationSerializer(items, many=True).data)

class NotificationUnreadCountView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'unread_count': NotificationService.unread_count(request.user)})

class NotificationMarkReadView(APIView):
    
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
    
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        updated = NotificationService.mark_all_read(request.user)
        return Response({'updated': updated})

class NotificationDeleteView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        notif = Notification.objects.filter(
            pk=pk, user=request.user, deleted_at__isnull=True
        ).first()
        if notif is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        NotificationService.delete(notif)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminBroadcastView(APIView):
    
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

class AdminBroadcastLogView(APIView):
    
    permission_classes = (IsAdminUser,)

    def get(self, request):
        qs         = BroadcastLogService.list_logs()
        paginator  = StandardPagination()
        page       = paginator.paginate_queryset(qs, request)
        serializer = BroadcastLogSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def delete(self, request):
        deleted = BroadcastLogService.clear_all()
        return Response(
            {'detail': f'{deleted} رکورد لاگ پاک شد.', 'deleted': deleted},
            status=status.HTTP_200_OK,
        )
