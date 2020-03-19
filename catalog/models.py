from django.db import models

from .helpers import get_unique_filename


class Image(models.Model):
    file = models.ImageField(upload_to=get_unique_filename)
    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=500)
    created = models.DateField()

    def __str__(self):
        return self.name
