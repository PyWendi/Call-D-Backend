from .commonImport import *
from ..serialisers_class.userSerializer import (
    LawyerSerialiser,
    ShortLawyerSerializer,
    ProfileImageSerializer,
    CvSerializer,
    AvailabilitySerializer)
from ..serialisers_class.experienceSerializer import ExperienceSerializer
from django.contrib.auth.hashers import make_password
from ..models import Domain, Region


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
        request_body=LawyerSerialiser,
        responses={201: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def create(self, request, *args, **kwargs):
        av_data = '[' + ("[false,false,false,false,false,false,false,false,false,false],"*4) + "[false,false,false,false,false,false,false,false,false,false]" + "]"

        domains = Domain.objects.filter(id__in=request.data.pop("domains"))
        region = Region.objects.get(pk=request.data.pop("region"))
        password = make_password(request.data.pop("password"))
        new_user = get_user_model().objects.create(**request.data, password=password, region=region, availability=av_data)
        for domain in domains:
            new_user.domains.add(domain)
        new_user.save()
        # print(f"\nHere is the domain objects :\n {domain}\n")
        print(new_user)
        serializer = LawyerSerialiser(new_user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=LawyerSerialiser,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    def update(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.first_name = request.data.get("first_name")
        user.last_name = request.data.get("last_name")
        user.phone = request.data.get("phone")
        user.location = request.data.get("location")
        # user.availability = request.data.get("availability")
        user.region = Region.objects.get(pk=request.data.pop("region"))
        user.domains.clear()
        domains = Domain.objects.filter(id__in=request.data.pop("domains"))
        for domain in domains:
            user.domains.add(domain)
        user.save()
        serializer = LawyerSerialiser(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        methods=["PUT"],
        request_body=ProfileImageSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=False, parser_classes=[MultiPartParser, FormParser],
            serializer_class=ProfileImageSerializer)
    def update_profile_image(self, request):
        user = request.user
        profile_img = request.FILES.get("profile_img") if request.FILES.get("profile_img") else None
        data = {"profile_img": profile_img}

        serializer = ProfileImageSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=CvSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=False, parser_classes=[MultiPartParser, FormParser],
            serializer_class=CvSerializer)
    def upload_cv(self, request):
        user = request.user
        cv_file = request.FILES.get("cv_file") if request.FILES.get("cv_file") else None
        data = {"cv_file": cv_file}

        serializer = CvSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=AvailabilitySerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=False, serializer_class=AvailabilitySerializer)
    def update_availability(self, request):
        user = request.user
        availability = request.data.get("availability")
        data = {"availability": availability}
        serializer = AvailabilitySerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True, serializer_class=AvailabilitySerializer)
    def get_availability(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        serializer = AvailabilitySerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=True)
    def get_experience(self, request, pk):
        # user = await get_object_or_404(get_user_model(), pk=pk)
        user = get_object_or_404(get_user_model(), pk=pk)
        experience = user.experience_set.all()

        serializer = ExperienceSerializer(experience, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        methods=["PUT"],
        request_body=ExperienceSerializer,
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["put"], detail=True)
    def download_file(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=request.user.id)
        # Use FileResponse to serve the file
        # The as_attachment=True parameter prompts the browser to download the file
        # return FileResponse(uploaded_file.file.open(), as_attachment=True)
        return Response({
            "file_link": user.cv_file.url
        })

    @swagger_auto_schema(
        methods=["GET"],
        responses={200: "OK", 400: "BAD request", 500: "SERVER ERROR"}
    )
    @action(methods=["GET"], detail=False)
    def get_all_lawyer(self, request, *args, **kwargs):
        lawyers = get_user_model().objects.filter(isClient=False)
        serializer = ShortLawyerSerializer(lawyers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            lawyers = get_user_model().objects.filter(first_name__icontains=search, isClient=False)
            # data = ShortLawyerSerializer(lawyers, many=True) if len(lawyers) > 0 else []
            data = []
            if len(lawyers) > 0:
                serializer = ShortLawyerSerializer(lawyers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "Error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
