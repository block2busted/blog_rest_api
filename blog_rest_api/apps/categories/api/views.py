from rest_framework import generics
from rest_framework import permissions

from .serializers import CategoryListSerializer, CategoryDetailSerializer
from categories.models import Category


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'