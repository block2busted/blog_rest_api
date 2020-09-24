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
    path('<int:pk>/', ArticleDetailAPIView.as_view(), name='article-details'),
    path('<int:pk>/create/', ArticleCreateAPIView.as_view(), name='article-create'),
    path('<int:pk>/update/', ArticleUpdateAPIView.as_view(), name='article-update'),
    path('<int:pk>/delete/', ArticleDeleteAPIView.as_view(), name='article-delete'),
]
