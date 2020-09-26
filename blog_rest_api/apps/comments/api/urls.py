from django.urls import path

from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
    CommentCreateAPIView
)


app_name = 'comments-api'
urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='details'),
    path('create/', CommentCreateAPIView.as_view(), name='create'),
]
