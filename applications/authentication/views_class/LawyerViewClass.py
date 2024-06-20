from .commonImport import *
from ..serialisers_class.userSerializer import LawyerSerialiser, ProfileImageSerializer, CvSerializer
from ..serialisers_class.experienceSerializer import ExperienceSerializer


class LawyerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = LawyerSerialiser
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m not in ['delete']]

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return super(LawyerViewSet, self).get_permissions()

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
    def update_profile_image(self, request, pk):
        # user = await get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}

        serializer = self.serializer_class(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=CvSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=True, parser_classes=[MultiPartParser, FormParser],
            serializer_class=CvSerializer)
    def upload_cv(self, request, pk):
        # user = await get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        cv_file = request.FILES.get("cv_file") if request.FILES.get("cv_file") else None
        data = {"cv_file": cv_file}

        serializer = self.serializer_class(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=ExperienceSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=True)
    def get_experience(self, request):
        # user = await get_object_or_404(get_user_model(), pk=pk)
        user = request.user
        experience = user.experience_set.all()

        serializer = ExperienceSerializer(experience, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
