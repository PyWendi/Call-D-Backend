from .commonImport import *
from ..serialisers_class.experienceSerializer import ExperienceSerializer
from ..models import Experience


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


