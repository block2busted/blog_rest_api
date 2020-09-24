from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions

from .serializers import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleCreateUpdateDeleteSerializer
)
from .paginations import ArticleListPagination
from articles.models import Article


class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()
    pagination_class = ArticleListPagination


class ArticleDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.all()


class ArticleCreateAPIView(generics.CreateAPIView):
    serializer_class = ArticleCreateUpdateDeleteSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = Article.objects.all()


class ArticleUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ArticleCreateUpdateDeleteSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = Article.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return serializer.save()


class ArticleDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ArticleCreateUpdateDeleteSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = Article.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None