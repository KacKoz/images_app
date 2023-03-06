from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Tier(models.Model):
    name = models.CharField(max_length=30)
    original_image_access = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

class UserTier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)

class TierThumbnailSize(models.Model):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    size = models.IntegerField()
