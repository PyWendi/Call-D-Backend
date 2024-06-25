from .commonImport import *
from ..serialisers_class.AppointmentSerializerClass import AppointmentSerializer
from ..models import Appointment, Notification
from applications.authentication.models import Speciality


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AppointmentSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        # appointment = Appointment
        lawyer = data.pop("lawyer")
        lawyer = get_user_model().objects.get(pk=int(lawyer))
        speciality = data.pop("speciality")
        speciality = Speciality.objects.get(pk=int(speciality))
        appointment = Appointment.objects.create(
            lawyer=lawyer,
            speciality=speciality,
            isConfirmed=False,
            isArchived=False,
            isValid=True,
            client_id=request.user.id,
            **data
        )
        appointment.save()
        """
        Part of notification
        """
        Notification.objects.create(
            author=request.user.id,
            receiver=lawyer,
            type="demande",
            appointment_id=appointment.id,
        )

        serializer = self.serializer_class(appointment, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        methods=["PUT"],
        # request_body=AppointmentSerializer,
        responses={200: "OK", 400: "BAD reque   st", 500: "SERVER ERROR"}
    )
    @action(methods=["PUT"], detail=True)
    def validate_appointment(self, request, pk, *args, **kwargs):
        """
        Only require `date` and `message`
        """
        date = request.data.get("date")
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.message = request.data.get("message", "")
        appointment.date = date
        appointment.isConfirmed = True
        appointment.save()
        """
        Part for sending notification
        Assuming the user is a lawyer.
        """
        Notification.objects.create(
            author=request.user.id,
            receiver=get_user_model().objects.get(pk=appointment.client_id),
            type="confirmation",
            appointment_id=appointment.id,
        )

        serializer = self.serializer_class(appointment, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def cancel_appointment(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.isValid = False
        appointment.save()
        """
        Part of notification 
        """
        Notification.objects.create(
            author=request.user.id,
            receiver=appointment.lawyer,
            type="annulation",
            appointment_id=appointment.id,
        )

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def archive(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.isArchived = True
        appointment.save()
        return Response(status=status.HTTP_200_OK)


    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, url_path="for/lawyer")
    def getAppointmentForLawyer(self, request):
        appointments = Appointment.objects.filter(lawyer=request.user)

        if len(appointments) > 0:
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=[], status=status.HTTP_200_OK)



    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, url_path="for/client")
    def getAppointmentForClient(self, request):
        appointments = Appointment.objects.filter(client_id=request.user.pk)

        if len(appointments) > 0:
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=[], status=status.HTTP_200_OK)
