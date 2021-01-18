# Create your views here.
from rest_framework import viewsets

from .models import Nsfw
from .serializers import (Base64NsfwSerializer, FileNsfwSerializer,
                          URLNsfwSerializer)


class NsfwViewSet(viewsets.ModelViewSet):
    queryset = Nsfw.objects.all()

    def get_serializer_class(self):
        input_type = self.request.data.get('type')
        if input_type == 'url':
            return URLNsfwSerializer
        elif input_type == 'base64':
            return Base64NsfwSerializer
        return FileNsfwSerializer
