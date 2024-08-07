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
        """
        This api expect the following data:
        `lawyer: integer,`
        `speciality: integer`,
        `title: string`,
        `description: string`
        """
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
        responses={200: AppointmentSerializer, 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, url_path="for/client")
    def getAppointmentForClient(self, request):
        appointments = []
        if request.user.isClient:
            appointments = Appointment.objects.filter(client_id=request.user.pk)
        else:
            appointments = Appointment.objects.filter(lawyer=request.user)

        if len(appointments) > 0:
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=[], status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: AppointmentSerializer, 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, url_path="archived/for/client")
    def getArchivedAppointmentForClient(self, request):
        appointments = []
        if request.user.isClient:
            appointments = Appointment.objects.filter(client_id=request.user.pk, isArchived=True)
        else:
            appointments = Appointment.objects.filter(lawyer=request.user, isArchived=True)

        if len(appointments) > 0:
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=[], status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, url_path="search/(?P<search>[a-zA-Z]+)")
    def lookup(self, request, search=None):
        """
        _summary_
        ```
        #This API is used to search lawyer by their first_name which is inserted in the url
        @request -> str:[a-zA-Z]+
        ```
        """
        try:
            if not search.isalpha():
                return Response({
                    "Error": "La recherche doit seulement contenir des carateres alphabetiques."
                }, status=status.HTTP_400_BAD_REQUEST)
            if request.user.isClient:
                appointments = Appointment.objects.filter(title__icontains=search, client_id=request.user.pk, isArchived=False)
            else:
                appointments = Appointment.objects.filter(title__icontains=search, lawyer=request.user, isArchived=False)

            # data = ShortLawyerSerializer(lawyers, many=True) if len(lawyers) > 0 else []
            data = []
            if len(appointments) > 0:
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "Error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False, url_path="search/archive/(?P<search>[a-zA-Z]+)")
    def lookupArchived(self, request, search=None):
        """
        _summary_
        ```
        #This API is used to search lawyer by their first_name which is inserted in the url
        @request -> str:[a-zA-Z]+
        ```
        """
        try:
            if not search.isalpha():
                return Response({
                    "Error": "La recherche doit seulement contenir des carateres alphabetiques."
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user.isClient:
                appointments = Appointment.objects.filter(title__icontains=search, client_id=request.user.pk, isArchived=True)
            else:
                appointments = Appointment.objects.filter(title__icontains=search, lawyer=request.user, isArchived=True)

            # data = ShortLawyerSerializer(lawyers, many=True) if len(lawyers) > 0 else []
            data = []
            if len(appointments) > 0:
                serializer = AppointmentSerializer(appointments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "Error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)