from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import SwaggerResponseUserSignupSerializer, UserSignupSerializer


class SignupAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="사용자 회원가입",
        request_body=UserSignupSerializer,
        responses={
            status.HTTP_201_CREATED: SwaggerResponseUserSignupSerializer,
            status.HTTP_400_BAD_REQUEST: "error",
        },
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
