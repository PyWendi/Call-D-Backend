from django.db import models
from applications.authentication.models_class.speciality import Speciality
from applications.authentication.models import CustomUser


class Appointment(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    message = models.TextField(null=True, blank=True)  # Filled during confirmation by the lawyer
    date = models.DateTimeField(blank=False)

    isConfirmed = models.BooleanField(default=False)
    isArchived = models.BooleanField(default=False)
    isValid = models.BooleanField(default=True)

    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)  # Foreign key to speciality
    lawyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Foreign to custom user (avocat)

    client_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
