from rest_framework import serializers
from ..models import Domain
from .specialitySerializer import SpecialitySerializer


class UserDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"


class DomainSerializer(serializers.ModelSerializer):
    specialities = SpecialitySerializer(source="speciality_set", many=True)
    class Meta:
        model = Domain
        fields = "__all__"
