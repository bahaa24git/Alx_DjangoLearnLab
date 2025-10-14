from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # unread first, then recent
        return Notification.objects.filter(recipient=self.request.user).order_by("read", "-created_at")


class MarkNotificationReadView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def patch(self, request, *args, **kwargs):
        notif = self.get_object()
        notif.read = True
        notif.save(update_fields=["read"])
        return Response({"id": notif.id, "read": True}, status=status.HTTP_200_OK)
