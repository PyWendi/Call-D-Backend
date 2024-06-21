from django.db import models
from .domain import Domain
from .customuser import CustomUser
from .speciality import Speciality


class Experience(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = models.TextField()

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True)
    specialities = models.ManyToManyField(Speciality)

    date_beg = models.DateField(null=False, blank=True)
    date_end = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.title
