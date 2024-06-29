from rest_framework import serializers
from applications.authentication.serialisers_class.specialitySerializer import SpecialitySerializer
from applications.authentication.serialisers_class.userSerializer import (
    ClientSerialiser,
    ClientForNotificationSerializer
)
from django.contrib.auth import get_user_model
from applications.appointment.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(many=False)
    lawyer = ClientForNotificationSerializer(many=False)
    client = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        # fields = "__all__"
        fields = [
            "title", "description", "message", "date",
            "isConfirmed", "isArchived", "isValid",
            "speciality", "lawyer", "client", "client_id", "created_at"
        ]

    def get_client(self, obj):
        clientId = obj.client_id
        try:
            client_instance = get_user_model().objects.get(id=clientId)
            serialiser = ClientForNotificationSerializer(client_instance)
            return serialiser.data
        except get_user_model().DoesNotExist:
            return None


class AppointmentForNotificationSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(many=False)
    client = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        exclude = ["lawyer", "client_id", "isConfirmed", "isArchived", "isValid",]
        # fields = "__all__"

    def get_client(self, obj):
        clientId = obj.client_id
        try:
            client_instance = get_user_model().objects.get(id=clientId)
            serialiser = ClientForNotificationSerializer(client_instance)
            return serialiser.data
        except get_user_model().DoesNotExist:
            return None