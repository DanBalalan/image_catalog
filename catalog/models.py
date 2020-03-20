import os

from django.db import models
from django.dispatch import receiver
from .helpers import get_unique_filename


class Image(models.Model):
    file = models.ImageField(upload_to=get_unique_filename)
    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=500)
    created = models.DateField()

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Image)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

