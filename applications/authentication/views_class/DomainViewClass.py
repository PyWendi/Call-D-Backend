from .commonImport import *
from ..models_class.domain import Domain
from ..serialisers_class.domainSerializer import UserDomainSerializer, DomainSerializer


class DomainViewSet(viewsets.ModelViewSet):
    serializer_class = UserDomainSerializer
    queryset = Domain.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method="GET",
        responses=({
            200: "OK, List of domain with speciality", 400: "Erreur innatendue", 500: "Erreur innatendu du serveur"
        }),
        # operation_summary="Les donnees envoyer dans le corps de la request (purchaseId) est utiliser pour creed des notification qui seront envoyer vers les administrateurs"
    )
    @action(methods=["GET"], detail=True)
    def get_speciality(self, request, pk, *args, **kwargs):
        """
        Retrieves all speciality linked for the authenticated user.
        This endpoint is intended for use in the user profile section.
        """
        domain = Domain.objects.get(pk=pk)
        domain_serializer = DomainSerializer(domain, many=False)
        return Response(domain_serializer.data, status=status.HTTP_200_OK)
