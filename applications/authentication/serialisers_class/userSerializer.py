from rest_framework import serializers
from django.contrib.auth import get_user_model
from .domainSerializer import UserDomainSerializer


class LawyerSerialiser(serializers.HyperlinkedModelSerializer):
    domains = UserDomainSerializer(many=True, source="domain_set")
    profile_img = serializers.ImageField(read_only=True)
    cv_file = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"

    def create(self, validated_data):
        user = get_user_model()
        return user.objects.create_user(**validated_data)


class ClientSerialiser(serializers.HyperlinkedModelSerializer):
    profile_img = serializers.ImageField(read_only=True)
    cv_file = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)
    is_staff = serializers.BooleanField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"
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
