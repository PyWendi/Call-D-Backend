from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .routers import router

urlpatterns = [
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

