from .commonImport import *
from ..serialisers_class.userSerializer import ClientSerialiser, ProfileImageSerializer, CvSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ClientSerialiser
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete']]

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return super(ClientViewSet, self).get_permissions()

    def get_authenticators(self):
        """
        Instantiates and returns the list of authentication classes that this view requires.
        """
        request_method = self.request.method.lower()
        if request_method == 'post':
            return []
        else:
            return [JWTAuthentication()]
        # return super(UserViewSet, self).get_authenticators()

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=ProfileImageSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=True, parser_classes=[MultiPartParser, FormParser],
            serializer_class=ProfileImageSerializer)
    async def update_profile_image(self, request, pk):
        # user = await get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}

        serializer = self.serializer_class(user, data=data)
        if serializer.is_valid():
            await serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

