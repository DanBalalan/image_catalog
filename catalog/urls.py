from django.urls import path
from .views import ImageUploadView, CatalogView, ImageDetailView, ImageDeleteView, ImageSearchView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='uploadimage'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('detail/<int:image_id>', ImageDetailView.as_view(), name='imagedetail'),
    path('delete/<int:image_id>', ImageDeleteView.as_view(), name='imagedelete'),
    path('search/', ImageSearchView.as_view(), name='imagesearch'),
]
