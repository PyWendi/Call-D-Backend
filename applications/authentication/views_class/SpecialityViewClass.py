from .commonImport import *
from ..serialisers_class.specialitySerializer import SpecialitySerializer
from ..models import Speciality, Domain


class SpecialityViewSet(viewsets.ModelViewSet):
    """
    Speciality wait the following data:
    `name`, `domain`
    """
    serializer_class = SpecialitySerializer
    queryset = Speciality.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SpecialitySerializer,
        responses={201: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def create(self, request, *args, **kwargs):
        domain = Domain.objects.get(pk=request.data.get("domain"))
        speciality = Speciality.objects.create(domain=domain, name=request.data.get("name"))
        serializer = self.serializer_class(speciality, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="GET",
        responses=({
            200: "OK, List of speciality linked to a domain", 400: "Erreur innatendue", 500: "Erreur innatendu du serveur"
        }),
        # operation_summary="Les donnees envoyer dans le corps de la request (purchaseId) est utiliser pour creed des notification qui seront envoyer vers les administrateurs"
    )
    @action(methods=["GET"], detail=False, url_path="by/domain/(?P<domain_id>[^/.]+)")
    def get_speciality_by_domain(self, request, domain_id: int, *args, **kwargs):
        """
        Retrieves all speciality linked for the authenticated user.
        This endpoint is intended for use in the user profile section.
        """
        # domain = Speciality.objects.all()
        # domain_serializer = DomainSerializer(domain, many=True)
        # return Response(domain_serializer.data, status=status.HTTP_200_OK)
        specialities = Speciality.objects.filter(domain=domain_id)
        serializer = SpecialitySerializer(specialities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
