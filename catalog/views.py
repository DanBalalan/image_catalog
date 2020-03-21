from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import ImageForm, ImageUpdateForm, ImageSearchForm
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
        form = ImageSearchForm()
        images = Image.objects.all()
        return render(request, 'catalog.html', {'images': images, 'form': form})


class ImageDetailView(View):

    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        form = ImageUpdateForm(instance=image)
        return render(request, 'image.html', {'image': image, 'form': form})

    def post(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        form = ImageUpdateForm(request.POST)
        if form.is_valid():
            image.name = form.cleaned_data['name']
            image.description = form.cleaned_data['description']
            image.created = form.cleaned_data['created']
            image.save()
            return HttpResponse('updated successfully')
        else:
            return HttpResponse('error: invalid form data')


class ImageDeleteView(View):

    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        image.delete()
        return HttpResponse('image deleted')


class ImageSearchView(View):

    def post(self, request):
        form = ImageSearchForm(request.POST)
        if form.is_valid():
            search_name = form.cleaned_data['name']
            search_description = form.cleaned_data['description']
            search_created = form.cleaned_data['created']
            qs = Image.objects.all()
            if search_name:
                qs = qs.filter(name__iexact=search_name)
            if search_description:
                qs = qs.filter(description__icontains=search_description)
            if search_created:
                qs = qs.filter(created=search_created)
            return render(request, 'catalog.html', {'images': qs, 'form': form, 'search': True})
        else:
            return HttpResponse('invalid form data')
