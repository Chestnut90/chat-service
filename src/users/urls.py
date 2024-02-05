from django.urls import path

from users.views import (
    SignupAPIView,
    TokenBlackListAPIView,
    TokenObtainPairAPIView,
    TokenRefreshAPIView,
    TokenVerifyAPIView,
)

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("token/", TokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyAPIView.as_view(), name="token_verify"),
    path("token/blacklist/", TokenBlackListAPIView.as_view(), name="token_blacklist"),
]
