from django.urls import path

from .views import (
    SignUpAPIView,
    LoginAPIView,
    UserDetailAPIView,
    LogoutAPIVew
)


app_name = 'accounts-api'
urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view(), name='sign-up'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIVew.as_view(), name='logout'),
    path('<str:username>/profile/', UserDetailAPIView.as_view(), name='profile')
]