from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, NotificationViewset, ContactViewSet

from .views_class.LawyerViewClass import LawyerViewSet
from .views_class.ClientViewClass import ClientViewSet
from .views_class.DomainViewClass import DomainViewSet
from .views_class.ExperienceViewClass import ExperienceViewSet
from .views_class.RegionViewClass import RegionViewSet
from .views_class.SpecialityViewClass import SpecialityViewSet

router = DefaultRouter()
router.register(r"lawyer", LawyerViewSet, basename="lawyer")
router.register(r"client", ClientViewSet, basename="client")
router.register(r"speciality", SpecialityViewSet, basename="speciality")
router.register(r"domain", DomainViewSet, basename="domain")
router.register(r"experience", ExperienceViewSet, basename="experience")
router.register(r"region", RegionViewSet, basename="region")
