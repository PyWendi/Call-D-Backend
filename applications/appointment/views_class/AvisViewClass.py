from .commonImport import *
from ..serialisers_class.AvisSerializerClass import AvisSerializer
from ..models import Avis


class AvisViewSet(viewsets.ModelViewSet):
    serializer_class = AvisSerializer
    queryset = Avis.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        methods=["POST"],
        request_body=AvisSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def create(self, request, *args, **kwargs):
        lawyerId = request.data.pop("lawyer")
        # lawyer = get_object_or_404(get_user_model(), pk=int(lawyerId))
        data = request.data
        avis = Avis.objects.create(lawyer=lawyerId, **data)
        serializer = self.serializer_class(avis, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
