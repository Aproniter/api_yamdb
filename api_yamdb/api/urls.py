from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, ReviewViewSet, TitleViewSet,
    UsersViewSet, registration, get_token
)

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
        registration,
        name='registration'
    ),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router.urls)),
]
