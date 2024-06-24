from .commonImport import *
from ..serialisers_class.AvisSerializerClass import AvisSerializer
from ..models import Avis, Notification


class AvisViewSet(viewsets.ModelViewSet):
    serializer_class = AvisSerializer
    queryset = Avis.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def create(self, request, *args, **kwargs):
        lawyer = get_object_or_404(get_user_model(), pk=int(request.data.pop("lawyer")))
        data = request.data
        avis = Avis.objects.create(lawyer=lawyer, writer=request.user.id, **data)
        """
                Part of notification 
                """
        Notification.objects.create(
            author=request.user.id,
            receiver=lawyer,
            type="annulation",
        )

        serializer = self.serializer_class(avis, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def for_lawyer(self, request, pk, *args, **kwargs):
        lawyer = get_object_or_404(get_user_model(), pk=pk)
        avis = Avis.objects.filter(lawyer=lawyer)

        if len(avis) > 0:
            serializer = AvisSerializer(avis, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(data=[], status=status.HTTP_200_OK)
