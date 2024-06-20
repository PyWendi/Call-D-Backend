from .commonImport import *
from ..serialisers_class.regionSerializer import RegionSerializer
from ..models import Region


class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
