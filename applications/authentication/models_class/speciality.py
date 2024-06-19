from django.db import models
from .domain import Domain


class Speciality(models.Model):
    name = models.CharField(max_length=200, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
