from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Image
import imghdr

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('user', 'image')

    def validate_image(self, image):
        if not image.name.endswith(('.jpg', '.png', '.jpeg')):
            raise ValidationError('Image name must end with .jpg or .png')
        if imghdr.what(image) not in ('jpeg', 'png'):
            raise ValidationError("Image should be in JPEG or PNG format " + str(imghdr.what(image)))
        return image
