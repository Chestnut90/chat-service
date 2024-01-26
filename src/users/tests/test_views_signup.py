from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SignupTestCase(APITestCase):
    url = reverse("signup")

    username = "user0"
    password = "zcAp!ssW0rd!"

    def test_signup_success(self):
        response = self.client.post(
            path=self.url,
            data={"username": self.username, "password": self.password},
        )

        # status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response no show user password
        self.assertIsNone(response.data.get("password", None))

        # password check
        user = get_user_model().objects.get(username=self.username)
        self.assertFalse(user.password == self.password)  # hashed
        self.assertTrue(user.check_password(self.password))  # correct password

    def test_signup_failed_missing_username(self):
        response = self.client.post(
            self.url,
            data={
                "username": self.username,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_failed_missing_password(self):
        response = self.client.post(
            path=self.url,
            data={
                "username": self.username,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_failed_password_validate(self):
        response = self.client.post(
            path=self.url,
            data={
                "username": self.username,
                "password": "1234",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
