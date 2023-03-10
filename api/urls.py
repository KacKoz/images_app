from django.urls import path
from .views import Images, ImageUrl, ExpiringLink

urlpatterns = [
    path('images', Images.as_view(), name='images'),
    path('images/<str:url>', ImageUrl.as_view(), name="image_url"),
    path('expiring', ExpiringLink.as_view(), name="expiring_link"),
]