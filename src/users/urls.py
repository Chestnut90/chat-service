from django.urls import path

from users.views import (
    SigninAPIView,
    SignoutAPIView,
    SignupAPIView,
    TokenRefreshAPIView,
    TokenVerifyAPIView,
    UserDeleteAPIView,
)

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("signin/", SigninAPIView.as_view(), name="signin"),
    path("token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyAPIView.as_view(), name="token_verify"),
    path("signout/", SignoutAPIView.as_view(), name="signout"),
    path("delete/", UserDeleteAPIView.as_view(), name="delete"),
]
