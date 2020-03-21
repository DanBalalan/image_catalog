from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import ImageForm
from .models import Image


class UploadImageView(View):

    def get(self, request):
        form = ImageForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Image(
                file=form.cleaned_data['file'],
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                created=form.cleaned_data['created']
            )
            instance.save()
            return HttpResponse('image uploaded')
        else:
            return HttpResponse('Upload Error: invalid form data')


class CatalogView(View):

    def get(self, request):
        images = Image.objects.all()
        return render(request, 'catalog.html', {'images': images})


class ImageDetailView(View):

    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        return render(request, 'image.html', {'image': image})


class ImageDeleteView(View):

    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        image.delete()
        return HttpResponse('image deleted')
