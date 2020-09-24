from django.urls import path

from .views import (
    ArticleListAPIView,
    ArticleDetailAPIView,
    ArticleCreateAPIView,
    ArticleUpdateAPIView,
    ArticleDeleteAPIView
)


app_name = 'articles-api'
urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='article-list'),
    path('create/', ArticleCreateAPIView.as_view(), name='article-create'),
    path('<str:slug>/', ArticleDetailAPIView.as_view(), name='article-details'),
    path('<str:slug>/update/', ArticleUpdateAPIView.as_view(), name='article-update'),
    path('<str:slug>/delete/', ArticleDeleteAPIView.as_view(), name='article-delete'),
]
