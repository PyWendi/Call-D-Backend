from .commonImport import *
from ..serialisers_class.NotificationSerializerClass import NotificationSerializer
from ..models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=["PUT"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["PUT"], detail=True)
    def marked_as_seen(self, request, pk, *args, **kwargs):
        notif = get_object_or_404(Notification, pk=pk)
        notif.seen = True
        notif.save()
        serializer = NotificationSerializer(notif, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
