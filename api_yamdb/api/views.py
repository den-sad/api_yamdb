from rest_framework import viewsets
from reviews.models import Category, Genre, Title, User

from .serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer