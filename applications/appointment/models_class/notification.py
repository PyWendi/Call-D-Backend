from django.db import models
from applications.authentication.models import CustomUser
from .appointment import Appointment


class Notification(models.Model):
    TYPE_CHOICE = [
        ("demande", "Demande"),
        ("annulation", "Annulation"),
        ("confirmation", "Confirmation"),
        ("avis", "Avis"),
    ]

    author = models.BigIntegerField(null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]
