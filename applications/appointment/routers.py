from rest_framework.routers import DefaultRouter

from .views_class.AppointmentViewClass import AppointmentViewSet
from .views_class.NotificationViewClass import NotificationViewSet
from .views_class.AvisViewClass import AvisViewSet

router = DefaultRouter()
router.register(r"appointment", AppointmentViewSet, basename="appointment")
router.register(r"notification", NotificationViewSet, basename="notification")
router.register(r"avis", AvisViewSet, basename="avis")