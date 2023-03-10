import imghdr
from django.urls import reverse
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from django.utils.timezone import timedelta
from django.utils import timezone
from .models import Image, ImageLink


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('user', 'image')

    def validate_image(self, image):
        if not image.name.lower().endswith(('.jpg', '.png', '.jpeg')):
            raise ValidationError('Image name must end with .jpg or .png')
        img_format = imghdr.what(image)
        if not img_format or img_format.lower() not in ('jpeg', 'png'):
            raise ValidationError(
                "Image should be in JPEG or PNG format " + str(imghdr.what(image)))
        return image


class ExpiringDeltaSecondsField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        data = int(data)
        if not (300 <= data <= 30000):
            raise ValidationError('Expiring time must be between 300 and 30000')
        return timezone.now() + timedelta(seconds=data)

class ExpiringLinkSerializer(ModelSerializer):
    expiring = ExpiringDeltaSecondsField()
    class Meta:
        model = ImageLink
        fields = ('image', 'expiring')
