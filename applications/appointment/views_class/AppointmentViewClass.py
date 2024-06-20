from .commonImport import *
from ..serialisers_class.AppointmentSerializerClass import AppointmentSerializer
from ..models import Appointment


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=["GET"],
        request_body=AppointmentSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def validate_appointement(self, request, pk, *args, **kwargs):
        pass
