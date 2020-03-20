from django.urls import path
from .views import UploadImageView, CatalogView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='uploadimage'),
    path('catalog/', CatalogView.as_view(), name='catalog')
]
