from django.urls import path

from .views import CommentListAPIView


app_name = 'comments-api'
urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    #path('<int:pk>/update/', name='update'),
    #path('<int:pk>/', name='delete')
]
