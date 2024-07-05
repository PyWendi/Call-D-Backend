from .commonImport import *
from ..serialisers_class.experienceSerializer import ExperienceSerializer
from ..models import Experience, Domain, Speciality


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ExperienceSerializer,
        responses={201: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def create(self, request, *args, **kwargs):
        domain = Domain.objects.get(pk=request.data.pop("domain"))
        owner = get_object_or_404(get_user_model(), pk=request.user.id)
        speciality_ids = request.data.pop("specialities")
        specialities = Speciality.objects.filter(id__in=speciality_ids)
        experience = Experience.objects.create(domain=domain, owner=owner, **request.data)
        for speciality in specialities:
            experience.specialities.add(speciality)
        experience.save()
        serializer = ExperienceSerializer(experience, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ExperienceSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def update(self, request, pk, *args, **kwargs):
        domain = Domain.objects.get(pk=request.data.get("domain"))
        specialities = Speciality.objects.filter(id__in=request.data.get("specialities"))
        experience = get_object_or_404(Experience, pk=pk)
        experience.title = request.data.get("title")
        experience.description = request.data.get("description")
        experience.date_beg = request.data.get("date_beg")
        experience.date_end = request.data.get("date_end", None)
        experience.domain = domain
        experience.specialities.clear()
        for speciality in specialities:
            experience.specialities.add(speciality)
        experience.save()
        serializer = ExperienceSerializer(experience, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def for_lawyer(self, request, pk, *args, **kwargs):
        lawyer = get_object_or_404(get_user_model(), pk=pk)
        experiences = Experience.objects.filter(owner=lawyer)
        if len(experiences) > 0:
            serializer = ExperienceSerializer(experiences, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=[], status=status.HTTP_200_OK)

