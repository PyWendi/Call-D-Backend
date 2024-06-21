from .commonImport import *
from ..serialisers_class.NotificationSerializerClass import NotificationSerializer
from ..models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def marked_as_seen(self, request, pk, *args, **kwargs):
        notif = get_object_or_404(Notification, pk=pk)
        notif.seen = True
        notif.save()
        serializer = NotificationSerializer(notif, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False)
    def for_user(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(receiver=request.user)
        if len(notifications) != 0:
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

