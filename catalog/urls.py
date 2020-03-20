from django.urls import path
from .views import UploadImageView, CatalogView, ImageDetailView, ImageDeleteView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='uploadimage'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('detail/<int:image_id>', ImageDetailView.as_view(), name='imagedetail'),
    path('delete/<int:image_id>', ImageDeleteView.as_view(), name='imagedelete'),
]
