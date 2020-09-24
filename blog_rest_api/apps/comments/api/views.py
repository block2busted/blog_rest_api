from rest_framework import generics

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer
)
from comments.models import Comment


class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer