from rest_framework import serializers
from django.contrib.auth import get_user_model
from .domainSerializer import UserDomainSerializer
from ..models import Domain


class LawyerSerialiser(serializers.ModelSerializer):
    profile_img = serializers.ImageField(read_only=True)
    cv_file = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    is_active = serializers.BooleanField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False)
    is_superuser = serializers.BooleanField(write_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)

    domains = UserDomainSerializer(many=True)
    # domain_ids = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"
        # exclude = ["domains"]

    def create(self, validated_data):
        user = get_user_model().objects.create()
        user.save()
        return user


class ClientSerialiser(serializers.HyperlinkedModelSerializer):
    profile_img = serializers.ImageField(read_only=True)
    cv_file = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False)
    is_superuser = serializers.BooleanField(write_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = get_user_model()
        # fields = "__all__"
        exclude = ["domains", "availability"]

    def create(self, validated_data):
        user = get_user_model()
        return user.objects.create_user(**validated_data)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["profile_img"]


class CvSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["cv_file"]
