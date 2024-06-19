from django.db import models


class Region(models.Model):
    designation = models.CharField(max_length=30)

    def __str__(self):
        return self.designation
