from rest_framework_simplejwt.views import TokenObtainPairView
from ..serialisers_class.tokenSerializer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customise the token which will return within the api
    """
    serializer_class = CustomTokenObtainPairSerializer
