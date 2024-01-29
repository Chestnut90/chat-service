from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TokenObtainAPITestCase(APITestCase):
    token_url = reverse("token_obtain_pair")
    token_refresh_url = reverse("token_refresh")
    token_verify_url = reverse("token_verify")

    @classmethod
    def setUpTestData(cls):
        cls.username = "user"
        cls.password = "dsf!2Nas@3"

        get_user_model().objects.create_user(
            username=cls.username,
            password=cls.password,
        )

    def test_token_obtain_success(self):
        response = self.client.post(
            path=self.token_url,
            data={
                "username": self.username,
                "password": self.password,
            },
            # content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access", None))
        self.assertIsNotNone(response.data.get("refresh", None))

    def test_token_obatin_failed_no_fields(self):
        response = self.client.post(
            path=self.token_url,
            data={},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_obtain_failed_invalid_password(self):
        response = self.client.post(
            path=self.token_url,
            data={
                "username": self.username,
                "password": "",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
