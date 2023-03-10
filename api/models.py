from django.db import models
from users.models import User
from uuid import uuid4
from django.utils import timezone
# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")

def generate_unique_image_url():
    url = str(uuid4())[:8]
    while ImageLink.objects.filter(url=url).exists():
        url = (uuid4())[:8]
    return url

class ImageLink(models.Model):
    url = models.CharField(max_length=16, unique=True, default=generate_unique_image_url)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_original = models.BooleanField(default=False)
    size = models.IntegerField(null=True, blank=True, default=None)
    expiring = models.DateTimeField(null=True, blank=True, default=None)

    def is_expired(self):
        return self.expiring is not None and self.expiring < timezone.now()
