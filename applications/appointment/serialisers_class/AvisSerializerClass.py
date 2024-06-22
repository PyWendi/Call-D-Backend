from rest_framework import serializers
from applications.authentication.serialisers_class.userSerializer import ShortLawyerSerializer
from ..models import Avis
from django.contrib.auth import get_user_model


class AvisSerializer(serializers.ModelSerializer):
    lawyer = ShortLawyerSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Avis
        fields = "__all__"
