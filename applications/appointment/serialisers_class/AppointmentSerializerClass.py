from rest_framework import serializers
from applications.authentication.serialisers_class.specialitySerializer import SpecialitySerializer
from applications.authentication.serialisers_class.userSerializer import ClientSerialiser, LawyerSerialiser
from django.contrib.auth import get_user_model
from applications.appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(many=False)
    lawyer = LawyerSerialiser(many=False)
    client = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = "__all__"

    def get_client(self, obj):
        clientId = obj.client_id
        try:
            client_instance = get_user_model().objects.get(id=clientId)
            serialiser = ClientSerialiser(client_instance)
            return serialiser.data
        except get_user_model().DoesNotExist:
            return None
