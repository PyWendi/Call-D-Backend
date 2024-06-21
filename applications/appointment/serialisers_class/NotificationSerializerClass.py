from rest_framework import serializers
from applications.authentication.serialisers_class.userSerializer import ClientSerialiser
from django.contrib.auth import get_user_model
from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    receiver = ClientSerialiser(many=False)

    class Meta:
        model = Notification
        fields = "__all__"

    def create(self, validated_data):
        receiver = validated_data.pop("receiver")
        receiver = get_user_model().objects.get(pk=int(receiver))
        notification = Notification.objects.create(receiver=receiver, **validated_data)
