from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SignoutAPITestCase(APITestCase):
    url = reverse("signout")
    refresh_url = reverse("token_refresh")

    @classmethod
    def setUpTestData(cls):
        cls.username = "test-user"
        cls.password = "asdf!13azf@"

        get_user_model().objects.create_user(
            username=cls.username, password=cls.password
        )

    def setUp(self):
        url = reverse("signin")
        response = self.client.post(
            url,
            data={
                "username": self.username,
                "password": self.password,
            },
        )

        self.access = response.data["access"]
        self.refresh = response.data["refresh"]

    def test_signout_success(self):
        response = self.client.post(
            self.url,
            data={"refresh": self.refresh},
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post(
            self.url,
            data={
                "refresh": self.refresh,
            },
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_signout_failed_invalid_token(self):
        response = self.client.post(
            self.url,
            data={
                "refresh": "invalid.refresh.token",
            },
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_signout_failed_no_data(self):
        response = self.client.post(
            self.url,
            data={},
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
