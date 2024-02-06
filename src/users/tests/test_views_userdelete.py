from datetime import datetime

from django.contrib.auth import get_user_model
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserDeleteAPITestCase(APITestCase):
    url = reverse("delete")

    def setUp(self):
        self.username = f"user-{str(datetime.now())}"
        self.password = "dfjaskldfn@!@#a"
        get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

        signin_url = reverse("signin")
        response = self.client.post(
            path=signin_url,
            data={
                "username": self.username,
                "password": self.password,
            },
        )

        self.access = response.data["access"]
        self.refresh = response.data["refresh"]

        self.authorization = f"Bearer {self.access}"

    def test_delete_success(self):
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=self.authorization,
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        with self.assertRaises(Http404):
            get_object_or_404(
                get_user_model(),
                username=self.username,
            )

        # refresh token is invalid
        refresh_url = reverse("token_refresh")
        response = self.client.post(
            path=refresh_url,
            data={
                "refresh": self.refresh,
            },
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_failed_with_no_authorization(self):
        response = self.client.post(path=self.url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
