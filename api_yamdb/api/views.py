from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.utils import six
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from users.models import User

from reviews.models import Category, Genre, Review, Title
from reviews.mixins import CreateDestroyListMixinSet
from api.filters import TitleFilter
from api.permissions import (
    AdminModeratorAuthorPermission, IsAdminOrReadOnly,
    AdminOnly, AuthorPermission
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleReadSerializer, TitleWriteSerializer,
    UserSerializer, RoleSerializer, RegistrationSerializer,
    TokenSerializer
)


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.username) + six.text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()


@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email'],
        )
    except Exception:
        return Response(
                    request.data,
                    status=status.HTTP_400_BAD_REQUEST
                )
    message = account_activation_token.make_token(user)
    send_mail(
        'Код подтверждения', message,
        settings.EMAIL_HOST_USER,
        [request.data.get('email')],
        fail_silently=False
    )
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get('username')
    )
    if not account_activation_token.check_token(
            user, request.data.get('confirmation_code')
    ):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return Response(token)


class CategoryViewSet(CreateDestroyListMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateDestroyListMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


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
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
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
    serializer_class = UserSerializer
    permission_classes = [AdminOnly]
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    search_fields = ('^username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'put', 'post'],
        url_name='me',
        permission_classes=[AuthorPermission],
        serializer_class=RoleSerializer
    )
    def me(self, request):
        serializer = self.serializer_class(request.user)
        if request.method == 'PATCH':
            serializer = self.serializer_class(
                request.user,
                data=request.data,
                partial=True,
                context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
