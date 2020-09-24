from django.urls import path
from .views import (
    CategoryListAPIView,
    CategoryDetailAPIView,

)

app_name = 'categories-api'
urlpatterns = [
    path('', CategoryListAPIView.as_view(), name='category-list'),
    path('<str:slug>/', CategoryDetailAPIView.as_view(), name='category-details')
]
