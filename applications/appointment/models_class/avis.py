from django.db import models
from applications.authentication.models import CustomUser

class Avis(models.Model):
    writer = models.BigIntegerField(null=True)
    lawyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    preference = models.SmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
