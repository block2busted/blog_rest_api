from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import SignUpSerializer, LoginSerializer, UserDetailSerializer
from .permissions import AnonPermissionOnly

User = get_user_model()


class SignUpAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AnonPermissionOnly, )
    serializer_class = SignUpSerializer


class LoginAPIView(APIView):
    permission_classes = (AnonPermissionOnly, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutAPIVew(APIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        response_data = {'details': 'Log out success!'}
        return Response(response_data, status=HTTP_200_OK)


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

