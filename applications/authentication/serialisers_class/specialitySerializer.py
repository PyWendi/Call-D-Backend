from rest_framework import serializers
from ..models import Speciality, Domain


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = "__all__"
