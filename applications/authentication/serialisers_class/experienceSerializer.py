from rest_framework import serializers
from ..models import Experience, Speciality
from ..serialisers_class.domainSerializer import UserDomainSerializer
from ..serialisers_class.specialitySerializer import SpecialitySerializer


class ExperienceSerializer(serializers.ModelSerializer):
    domain = UserDomainSerializer(many=False)
    specialities = SpecialitySerializer(many=True, source="speciality_set")
    class Meta:
        model = Experience
        fields = "__all__"

    def create(self, validated_data):
        domain = validated_data.pop("domain", None)
        specialities = validated_data.pop("specialities", [])

        experience = Experience.objects.create(**validated_data)

        if domain is not None:
            experience.domain = domain

        if specialities.length != 0:
            for speciality in specialities:
                speciality_instance = Speciality.objects.get(pk=int(speciality))
                experience.specialities.add(speciality_instance)

        experience.save()
        return experience