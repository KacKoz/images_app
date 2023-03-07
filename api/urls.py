from django.contrib import admin
from django.urls import include, path
from .views import UploadFile

urlpatterns = [
    path('image', UploadFile.as_view(), name='image'),
]