from random import randint

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from users.models import User
from .serializers import RegistrationSerializer, TokenSerializer


def generate_code():
    return str(randint(10000, 99999))


class RegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        if User.objects.filter(email=request.data.get('email')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=request.data.get('username')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        message = generate_code()
        serializer.is_valid(raise_exception=True)
        send_mail(
            'Код подтверждения', message,
            settings.EMAIL_HOST_USER,
            [request.data.get('email')],
            fail_silently=False
        )
        serializer.validated_data['confirm_code'] = message
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenApiView(APIView):
    serializer_class = TokenSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if user.confirm_code != request.data.get('confirmation_code'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = self.get_tokens_for_user(user)
        user.token = token
        user.save()
        return Response(token, status=status.HTTP_200_OK)
