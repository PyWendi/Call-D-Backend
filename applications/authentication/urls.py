from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from .views_class.CustomTokenObtainPairViewClass import CustomTokenObtainPairView

from .routers import router

urlpatterns = [
    # Authentication url to take token
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("set_password/<str:password>", set_password, name="password_setter"),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
