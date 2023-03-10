from django.core.files import File
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from PIL import Image as PILImage
import io

from users.models import Tier, User, UserTier
from api.models import ImageLink, Image

# Create your tests here.


class UploadImagesTests(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            username='testuser', password='testpassword')
        tier = Tier.objects.create(name='testtier', original_image_access=True)
        UserTier.objects.create(user=user, tier=tier)
        return super().setUp()

    def test_upload_valid_image(self):
        img = PILImage.new('RGB', (100, 100))
        file = io.BytesIO()
        file.name = 'image.jpg'
        img.save(file, 'jpeg')
        file.seek(0)
        client = APIClient()
        user = User.objects.get(username='testuser')
        client.force_authenticate(user)
        response = client.post(reverse('images'), {'image': file})
        self.assertEqual(response.status_code, 200)

    def test_upload_invalid_image(self):
        file = io.BytesIO()
        file.name = 'image.jpg'
        file.write(b'0')
        file.seek(0)
        client = APIClient()
        user = User.objects.get(username='testuser')
        client.force_authenticate(user)
        response = client.post(reverse('images'), {'image': file})
        self.assertEqual(response.status_code, 400)


class GetImagesTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create(
            username='testuser', password='testpassword')
        tier = Tier.objects.create(name='testtier', original_image_access=True)
        UserTier.objects.create(user=user, tier=tier)
        img = PILImage.new('RGB', (100, 100))
        file = io.BytesIO()
        file.name = 'image.jpg'
        img.save(file, 'jpeg')
        file.seek(0)
        image = Image.objects.create(user=user, image=File(file))
        ImageLink.objects.create(image=image, is_original=True)
        return super().setUp()

    def test_get_images_list(self):
        client = APIClient()
        user = User.objects.get(username='testuser')
        client.force_authenticate(user)
        response = client.get(reverse('images'))
        self.assertTrue('images' in response.data)
        self.assertEqual(len(response.data['images']), 1)
        self.assertEqual(len(response.data['images'][0]['urls']), 1)
        self.assertEqual(response.data['images']
                         [0]['urls'][0]['size'], 'original')

class CreateExpiringLink(APITestCase):
    def setUp(self) -> None:
        img = PILImage.new('RGB', (100, 100))
        file = io.BytesIO()
        file.name = 'image.jpg'
        img.save(file, 'jpeg')
        file.seek(0)

        # user1
        user = User.objects.create(
            username='testuser', password='testpassword')
        tier = Tier.objects.create(name='testtier', original_image_access=True, expiring_link=True)
        UserTier.objects.create(user=user, tier=tier)
        image = Image.objects.create(user=user, image=File(file))
        self.image_id = image.pk
        ImageLink.objects.create(image=image, is_original=True)
        
        # user2
        user2 = User.objects.create(
            username='testuser2', password='testpassword')
        tier2 = Tier.objects.create(name='testtier2', original_image_access=True, expiring_link=False)
        UserTier.objects.create(user=user2, tier=tier2)
        image2 = Image.objects.create(user=user2, image=File(file))
        self.image2_id = image2.pk
        ImageLink.objects.create(image=image2, is_original=True)
        return super().setUp()

    def test_create_valid_expiring_link(self):
        client = APIClient()
        user = User.objects.get(username='testuser')
        client.force_authenticate(user)
        response = client.post(reverse('expiring_link'), {'expiring': 300, 'image': self.image_id})
        self.assertEqual(response.status_code, 200)
        response = client.post(reverse('expiring_link'), {'expiring': 30000, 'image': self.image_id})
        self.assertEqual(response.status_code, 200)    

    def test_create_invalid_expiring_link(self):
        client = APIClient()
        user = User.objects.get(username='testuser')
        client.force_authenticate(user)
        response = client.post(reverse('expiring_link'), {'expiring': 299, 'image': self.image_id})
        self.assertEqual(response.status_code, 400)
        response = client.post(reverse('expiring_link'), {'expiring': 30001, 'image': self.image_id})
        self.assertEqual(response.status_code, 400)
        client2 = APIClient()
        user2 = User.objects.get(username='testuser2')
        client2.force_authenticate(user2)
        response = client2.post(reverse('expiring_link'), {'expiring': 300, 'image': self.image_id})
        self.assertTrue(response.status_code, 401)
        response = client2.post(reverse('expiring_link'), {'expiring': 300, 'image': self.image2_id})
        self.assertTrue(response.status_code, 401)
        

