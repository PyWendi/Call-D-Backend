from rest_framework import serializers
from applications.authentication.serialisers_class.userSerializer import ClientForNotificationSerializer
from ..serialisers_class.AppointmentSerializerClass import AppointmentForNotificationSerializer
from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    receiver = ClientForNotificationSerializer(many=False)
    appointment = AppointmentForNotificationSerializer(many=False)

    class Meta:
        model = Notification
        fields = "__all__"
