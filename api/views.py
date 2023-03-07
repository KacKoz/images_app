from django.core.files.uploadedfile import InMemoryUploadedFile as File
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import ImageSerializer

# Create your views here.


class UploadFile(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = ImageSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data={'user': self.request.user.id, 'image': self.request.FILES.get('img')})
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return Response(status=status.HTTP_200_OK)
