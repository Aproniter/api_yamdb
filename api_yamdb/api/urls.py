from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import RegistrationApiView, TokenApiView, UsersViewSet

router = SimpleRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', RegistrationApiView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/', TokenApiView.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/', include(router.urls)),
]
