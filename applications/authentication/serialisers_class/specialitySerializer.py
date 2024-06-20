from rest_framework import serializers
from ..models import Speciality, Domain


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = "__all__"

    def create(self, validated_data):
        domain_id = validated_data.pop('domain', None)
        domain = None
        if domain_id is not None:
            try:
                domain = Domain.objects.get(id=domain_id)
            except Domain.DoesNotExist:
                raise serializers.ValidationError("Domain does not exist.")

        speciality = Speciality.objects.create(**validated_data)

        # If a domain was specified, associate it with the speciality
        if domain:
            speciality.domain = domain

        speciality.save()
        return speciality
