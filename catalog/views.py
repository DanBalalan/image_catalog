from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import Image


class UploadImageView(View):

    def get(self, request):
        form = ImageUploadForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Image(
                file=form.cleaned_data['image'],
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                created=form.cleaned_data['created']
            )
            instance.save()
            return HttpResponse('success')
        else:
            return HttpResponse('Upload Error: invalid form data')

