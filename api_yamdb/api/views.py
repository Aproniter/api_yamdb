from random import randint

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from users.models import User
from users.serializers import UsersSerializer, RegistrationSerializer, TokenSerializer
from reviews.models import Category, Genre, Review, Title
from reviews.mixins import ModelMixinSet
from api.filters import TitleFilter
from api.permissions import (
    AdminModeratorAuthorPermission, IsAdminOrReadOnly,
    AdminOnly, AuthorPermission
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleReadSerializer, TitleWriteSerializer
)


def generate_code():
    """Для создания кода подтверждения нужно использовать стандартные механизмы, это надёжнее и безопаснее
https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView
https://github.com/django/django/blob/master/django/contrib/auth/tokens.py#L107a"""
    return str(randint(10000, 99999))


class RegistrationApiView(APIView):
    """Вместо этого можно создать функцию отправления кода на имейл с помощью декоратора api_view
Точно также можно поступить и с jwt
Код станет лаконичнее :)
https://www.django-rest-framework.org/api-guide/views/#api_view"""
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
        if 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if user.confirm_code != request.data.get('confirmation_code'):
            """Лучше пользоваться стандартным механизмом
https://www.programcreek.com/python/example/99849/django.contrib.auth.tokens.default_token_generator.check_token"""
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = self.get_tokens_for_user(user)
        user.token = token
        user.save()
        return Response(token, status=status.HTTP_200_OK)


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    """Посмотрите на строки 93-96 и 102-105, они одинаковые, а ещё у этих классов общий родительский класс, так что стоит это вынести туда :)"""


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        """Здесь и ниже необходимо проверить, что ревью на верный тайтл. Это можно сделать с помощью указания дополнительного параметра в выборке title__id"""
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AdminOnly]
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    search_fields = ('^username',)
    """Здесь можно использовать декоратор action для me, чтобы не писать отдельный APIView"""


class UserApiView(APIView):
    serializer_class = UsersSerializer
    permission_classes = [AuthorPermission]

    def get(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            """Стоит воспользоваться https://www.django-rest-framework.org/api-guide/exceptions/#validationerror
И избавиться от if и вложенного блока"""
            if 'role' not in serializer.validated_data:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


