from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import CharField, ModelSerializer

from common.serializers import SwaggerResponseSerializerBase


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class SwaggerUserSignupResponseSerializer(SwaggerResponseSerializerBase):
    username = CharField()


class SwaggerTokenObtainPairResponseSerializer(SwaggerResponseSerializerBase):
    access = CharField()
    refresh = CharField()


class SwaggerTokenRefreshResponseSerializer(SwaggerResponseSerializerBase):
    access = CharField()
