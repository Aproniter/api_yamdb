from random import randint

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from users.models import User
from .serializers import RegistrationSerializer, TokenSerializer, UsersSerializer
from .permissions import IsAdminOrReadOnly


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

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly ]
    pagination_class = LimitOffsetPagination
    search_fields = ('^username',)



# from django.db.models import Avg
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from reviews.models import Category, Genre, Review, Title, User
# from api.filters import TitleFilter
# from .mixins import ModelMixinSet
# from .permissions import (
#     AdminModeratorAuthorPermission, AdminOnly, IsAdminUserOrReadOnly
# )
# from .serializers import (
#     CategorySerializer, CommentSerializer, GenreSerializer, GetTokenSerializer,
#     NotAdminSerializer, ReviewSerializer, SignUpSerializer, UsersSerializer,
#     TitleReadSerializer, TitleWriteSerializer
# )
#
#
# class UsersViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UsersSerializer
#     permission_classes = (IsAuthenticated, AdminOnly,)
#     lookup_field = 'username'
#     filter_backends = (SearchFilter, )
#     search_fields = ('username', )
#
#     @action(
#         methods=['GET', 'PATCH'],
#         detail=False,
#         permission_classes=(IsAuthenticated,)
#     )
#     def get_current_user_info(self, request):
#         serializer = UsersSerializer(request.user)
#         if request.method == 'PATCH':
#             if request.user.is_admin:
#                 serializer = UsersSerializer(
#                     request.user,
#                     data=request.data,
#                     partial=True)
#             else:
#                 serializer = NotAdminSerializer(
#                     request.user,
#                     data=request.data,
#                     partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.data)
#
#
# class APIGetToken(APIView):
#     def post(self, request):
#         serializer = GetTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
#         user = User.objects.get(username=data['username'])
#         token = RefreshToken.for_user(user).access_token
#         return Response({'token': str(token)}, status=status.HTTP_201_CREATED)
#
#
# class APISignup(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         serializer = SignUpSerializer(data=request.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class CategoryViewSet(ModelMixinSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (IsAdminUserOrReadOnly,)
#     filter_backends = (SearchFilter, )
#     search_fields = ('name', )
#     lookup_field = 'slug'
#
#
# class GenreViewSet(ModelMixinSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = (IsAdminUserOrReadOnly,)
#     filter_backends = (SearchFilter,)
#     search_fields = ('name', )
#     lookup_field = 'slug'
#
#
# class TitleViewSet(ModelViewSet):
#     queryset = Title.objects.annotate(
#         rating=Avg('reviews__score')
#     ).all()
#     permission_classes = (IsAdminUserOrReadOnly,)
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = TitleFilter
#
#     def get_serializer_class(self):
#         if self.action in ('list', 'retrieve'):
#             return TitleReadSerializer
#         return TitleWriteSerializer
#
#
# class CommentViewSet(ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (AdminModeratorAuthorPermission,)
#
#     def get_queryset(self):
#         review = get_object_or_404(
#             Review,
#             id=self.kwargs.get('review_id'))
#         return review.comments.all()
#
#     def perform_create(self, serializer):
#         review = get_object_or_404(
#             Review,
#             id=self.kwargs.get('review_id'))
#         serializer.save(author=self.request.user, review=review)
#
#
# class ReviewViewSet(ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = (AdminModeratorAuthorPermission,)
#
#     def get_queryset(self):
#         title = get_object_or_404(
#             Title,
#             id=self.kwargs.get('title_id'))
#         return title.reviews.all()
#
#     def perform_create(self, serializer):
#         title = get_object_or_404(
#             Title,
#             id=self.kwargs.get('title_id'))
#         serializer.save(author=self.request.user, title=title)
