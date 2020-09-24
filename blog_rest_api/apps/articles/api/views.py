from django.db.models import Q
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.filters import SearchFilter

from .serializers import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleDeleteSerializer,
    ArticleUpdateSerializer
)
from .paginations import ArticleListPagination
from articles.models import Article


class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = ArticleListPagination
    search_filter = (SearchFilter, )
    search_fields = ('title', 'content')

    def get_queryset(self, *args, **kwargs):
        queryset = Article.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
            ).distinct()
        return queryset



class ArticleDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'


class ArticleCreateAPIView(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = Article.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ArticleUpdateSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = Article.objects.all()
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class ArticleDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ArticleDeleteSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = Article.objects.all()
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None