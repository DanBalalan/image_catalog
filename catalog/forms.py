from django.forms import ModelForm, Form, fields
from .models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'name', 'description', 'created']


class ImageUpdateForm(ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'description', 'created']


class ImageSearchForm(ModelForm):
    name = fields.CharField(max_length=100, required=False)

    class Meta:
        model = Image
        fields = ['description', 'created']
