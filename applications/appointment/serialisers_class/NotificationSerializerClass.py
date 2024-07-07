from rest_framework import serializers
from django.contrib.auth import get_user_model
from applications.authentication.serialisers_class.userSerializer import ClientForNotificationSerializer
from ..serialisers_class.AppointmentSerializerClass import AppointmentForNotificationSerializer
from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    receiver = ClientForNotificationSerializer(many=False)
    appointment = AppointmentForNotificationSerializer(many=False)

    class Meta:
        model = Notification
        fields = "__all__"


class NotificationFetchSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    appointment = AppointmentForNotificationSerializer(many=False)

    class Meta:
        model = Notification
        fields = ["id",
                  "author",
                  "receiver",
                  "type",
                  "appointment",
                  "seen",
                  "created_at"]

    def get_author(self, obj):
        clientId = obj.author
        try:
            client_instance = get_user_model().objects.get(id=clientId)
            serialiser = ClientForNotificationSerializer(client_instance)
            return serialiser.data
        except get_user_model().DoesNotExist:
            return None