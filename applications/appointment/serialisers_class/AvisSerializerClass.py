from rest_framework import serializers
from applications.authentication.serialisers_class.userSerializer import LawyerSerialiser
from applications.appointment.models import Avis


class AvisSerializer(serializers.ModelSerializer):
    lawyer = LawyerSerialiser(many=False)

    class Meta:
        model = Avis
        fields = "__all__"

