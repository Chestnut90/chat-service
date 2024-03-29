from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.serializers import (
    SwaggerTokenObtainPairResponseSerializer,
    SwaggerTokenRefreshResponseSerializer,
    SwaggerUserSignupResponseSerializer,
    UserSignupSerializer,
)


class SignupAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="사용자 회원가입",
        request_body=UserSignupSerializer,
        responses={
            status.HTTP_201_CREATED: SwaggerUserSignupResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "error",
        },
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SigninAPIView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="사용자 토큰 발급",
        responses={
            status.HTTP_200_OK: SwaggerTokenObtainPairResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "error",
            status.HTTP_401_UNAUTHORIZED: "unauthorized",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshAPIView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="사용자 토큰 재발급",
        responses={
            status.HTTP_200_OK: SwaggerTokenRefreshResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "error",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyAPIView(TokenVerifyView):
    @swagger_auto_schema(
        operation_description="사용자 토큰 확인",
        responses={
            status.HTTP_200_OK: "ok",
            status.HTTP_400_BAD_REQUEST: "error",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SignoutAPIView(TokenBlacklistView):
    @swagger_auto_schema(
        operation_description="사용자 로그아웃, 토큰 만료",
        responses={
            status.HTTP_200_OK: "ok",
            status.HTTP_400_BAD_REQUEST: "required data",
            status.HTTP_401_UNAUTHORIZED: "Token is blacklisted",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="사용자 회원 탈퇴",
        operation_description="인증된 사용자로 부터 회원 탈퇴를 진행하고 발급된 토큰을 무효화",
        responses={
            status.HTTP_204_NO_CONTENT: "ok",
            status.HTTP_401_UNAUTHORIZED: "unauthorized",
        },
    )
    def post(self, request, *args, **kwargs):
        self.destory_user_tokens(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destory_user_tokens(self, user):
        tokens = OutstandingToken.objects.filter(user_id=user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        user.delete()
