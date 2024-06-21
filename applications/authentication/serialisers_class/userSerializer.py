from rest_framework import serializers
from .domainSerializer import UserDomainSerializer
from django.contrib.auth import get_user_model
from ..models import Domain, CustomUser


class LawyerSerialiser(serializers.ModelSerializer):
    profile_img = serializers.ImageField(read_only=True)
    cv_file = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    is_active = serializers.BooleanField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False)
    is_superuser = serializers.BooleanField(write_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)

    domains = UserDomainSerializer(many=True)

    class Meta:
        model = CustomUser()
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser().objects.create()
        user.save()
        return user


class ClientSerialiser(serializers.ModelSerializer):
    profile_img = serializers.ImageField(read_only=True)
    cv_file = serializers.FileField(read_only=True)
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False)
    is_superuser = serializers.BooleanField(write_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        model = CustomUser()
        # fields = "__all__"
        exclude = ["domains", "availability"]

    def create(self, validated_data):
        user = CustomUser
        return user.objects.create_user(**validated_data)


class ClientForNotificationSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(read_only=True)

    class Meta:
        model = CustomUser()
        fields = ["first_name", "last_name", 'profile_img']


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["profile_img"]


class CvSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["cv_file"]
