from rest_framework import serializers
from ..models import Experience, Speciality
from ..serialisers_class.domainSerializer import UserDomainSerializer
from ..serialisers_class.specialitySerializer import SpecialitySerializer


class ExperienceSerializer(serializers.ModelSerializer):
    domain = UserDomainSerializer(many=False)
    specialities = SpecialitySerializer(many=True)
    class Meta:
        model = Experience
        fields = "__all__"
