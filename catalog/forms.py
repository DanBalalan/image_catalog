from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500)
    created = forms.DateField()
