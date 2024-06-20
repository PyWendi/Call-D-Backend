from rest_framework import serializers
from applications.authentication.serialisers_class.specialitySerializer import SpecialitySerializer
from applications.authentication.serialisers_class.userSerializer import ClientSerialiser, LawyerSerialiser
from django.contrib.auth import get_user_model
from applications.appointment.models import Appointment
# from applications.authentication.models import Speciality


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

    # def create(self, validated_data):
    #     lawyer = validated_data.pop("lawyer")
    #     lawyer = get_user_model().objects.get(pk=int(lawyer))
    #     speciality = validated_data.pop("speciality")
    #     speciality = Speciality.objects.get(pk=int(speciality))
    #     appointment = Appointment.objects.create(
    #         lawyer=lawyer,
    #         speciality=speciality,
    #         isConfirmed=False,
    #         isArchived=False,
    #         isValid=True,
    #         **validated_data
    #     )
    #     appointment.save()
    #     return appointment

