from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to='catalog_files')
    name = models.CharField(null=False, max_length=100)
    description = models.CharField(null=True, max_length=500)
    created = models.DateField()
