from rest_framework import generics, mixins

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentDetailSerializer,
    CommentListSerializer,
    create_comment_serializer,
)
from comments.models import Comment


class CommentDetailAPIView(generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.parent_only()
    serializer_class = CommentListSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.parent_only()

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_pk = self.request.GET.get('parent_pk', None)
        serializer = create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_pk=parent_pk,
            user=self.request.user
        )
        return serializer


class CommentUpdateDeleteAPIView(generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None
