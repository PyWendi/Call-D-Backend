from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Local import (models)
from applications.authentication.models_class.domain import Domain
from applications.authentication.models_class.manager import CustomUserManager
from applications.authentication.models_class.region import Region


def upload_to(instance, filename):
    return "profile_images/" + filename


def upload_cv_to(instance, filename):
    return "cv_storage/" + filename


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=128)
    location = models.CharField(max_length=200, null=True, blank=True)
    isClient = models.BooleanField(default=False)

    profile_img = models.ImageField(upload_to=upload_to, blank=True, null=True)
    cv_file = models.FileField(upload_to=upload_cv_to, blank=True, null=True)
    availability = models.TextField(null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True) # relationship
    domains = models.ManyToManyField(Domain) # relationship

    date_joined = models.DateTimeField(auto_now_add=True, editable=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name
