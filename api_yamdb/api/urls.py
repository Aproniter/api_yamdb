from django.urls import path, include
from rest_framework.routers import SimpleRouter

from reviews.views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, ReviewViewSet, TitleViewSet
)
from .views import RegistrationApiView, TokenApiView
from users.views import UsersViewSet, UserApiView

app_name = 'api'

router = SimpleRouter()
router.register('^users', UsersViewSet, basename='users')

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
urlpatterns = [
    path(
        'v1/auth/signup/',
        RegistrationApiView.as_view(),
        name='registration'
    ),
    path('v1/auth/token/', TokenApiView.as_view(), name='get_token'),
    path('v1/users/me/', UserApiView.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
