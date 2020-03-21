from django.forms import ModelForm
from .models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'name', 'description', 'created']


class ImageUpdateForm(ModelForm):
    class Meta:
        model = Image
        fields = ['description', 'created']
