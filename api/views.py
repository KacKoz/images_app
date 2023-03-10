from django.http import FileResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Image, ImageLink
from users.models import UserTier, TierThumbnailSize
from .serializers import ExpiringLinkSerializer, ImageSerializer
from .utils import make_thumbnail
from images_app.settings import BASE_DIR
from PIL import Image as PILImage
import io

# Create your views here.


class Images(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    def get(self, request, format=None):
        images = Image.objects.filter(user=request.user)
        result = []
        for image in images:
            image_json = {
                'id': image.pk,
                'image': image.image.name.split('/')[-1],
                'urls': []
            }            
            links = ImageLink.objects.filter(image=image)
            for link in links:
                if link.is_expired():
                    continue
                image_json['urls'].append({
                    'url': request.build_absolute_uri(reverse('image_url', args=(link.url,))),
                    'size': 'original' if link.is_original else f'{link.size}px',
                    'expires': link.expiring
                })
            result.append(image_json)
        return Response({'images': result})

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data={'user': self.request.user.id, 'image': self.request.FILES.get('image')})
        if serializer.is_valid():
            image = serializer.save()
            try:
                user_tier = UserTier.objects.get(user=self.request.user)
            except UserTier.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            tier = user_tier.tier
            image_links: list[ImageLink] = []
            if tier.original_image_access:
                image_links.append(ImageLink(image=image, is_original=True))
            thumbnail_sizes = TierThumbnailSize.objects.filter(tier=tier)
            for thumbnail in thumbnail_sizes:
                if thumbnail.size <= image.image.height:
                    image_links.append(ImageLink(image=image, size=thumbnail.size))
            for link in image_links: link.save()
            return Response({'links': [{
                    'url': request.build_absolute_uri(reverse('image_url', args=(link.url,))),
                    'size': 'original' if link.is_original else f'{link.size}px'
                } for link in image_links
            ]}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageUrl(APIView):
    serializer_class = ImageSerializer

    def get(self, request, url, format=None):
        try:
            image_link = ImageLink.objects.get(url=url)
        except ImageLink.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if image_link.is_expired():
            return Response(status=status.HTTP_410_GONE)
        image_obj = self.serializer_class(image_link.image)
        try:
            image = PILImage.open(str(BASE_DIR) + image_obj.data.get('image'))
        except FileNotFoundError:
            return Response({'error': 'file not found'}, status=status.HTTP_404_NOT_FOUND)
        if not image_link.is_original:
            make_thumbnail(image, image_link.size)
        stream = io.BytesIO()
        image.save(stream, format=image.format)
        stream.seek(0)
        return FileResponse(stream, content_type=f"image/{image.format}")


class ExpiringLink(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExpiringLinkSerializer

    def post(self, request, format=None):
        user_tier = UserTier.objects.filter(user=self.request.user).first()
        if not user_tier or not user_tier.tier.expiring_link:
            return Response({'message': 'you can\'t create expiring links with your current plan'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('image').user != self.request.user:
                return Response({'message': 'this image belongs to another user'}, status=status.HTTP_401_UNAUTHORIZED)
            serializer.save(is_original=True)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
 