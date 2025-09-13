import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient


class ModelTests(TestCase):
    def test_create_superuser_success(self):
        superuser = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="superpass123"
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.check_password("superpass123"))

    def test_create_superuser_with_is_staff_false_raises_error(self):
        with self.assertRaises(ValueError) as e:
            get_user_model().objects.create_superuser(
                email="admin@example.com",
                password="superpass123",
                is_staff=False
            )
        self.assertIn("is_staff=True", str(e.exception))

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with self.assertRaises(ValueError) as e:
            get_user_model().objects.create_superuser(
                email="admin@example.com",
                password="superpass123",
                is_superuser=False
            )
        self.assertIn("is_superuser=True", str(e.exception))


# Create your tests here.
class AuthenticatedApiTests(TestCase):
    def get_user_url(self, user_path):
        return reverse(f"user:{user_path}")

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_register_user(self):
        response = self.client.post(
            self.get_user_url("create"),
            data={
                "email": "u@g.com",
                "password": "t2683gru"
            }
        )
        self.assertNotIn(str(response.data), "errors")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email="u@g.com")
        self.assertTrue(check_password("t2683gru", user.password))

    def test_update_user(self):
        response = self.client.put(
            self.get_user_url("manage"),
            data={
                "email": "updateu@g.com",
                "password": "t2683gru"
            }
        )

        self.assertNotIn("error", str(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.get(email="updateu@g.com")
        self.assertTrue(check_password("t2683gru", user.password))

    @patch("user.views.send_verification_email")
    def test_verify_user_email_sent(self, mock_send_email):
        response = self.client.post(
            self.get_user_url("email_verify"),
        )
        self.assertNotIn("error", str(response.data))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = get_user_model().objects.get(email="test@test.com")
        self.assertIsNotNone(user.verification_code)
        self.assertIsNotNone(user.verification_code_timeout)

        mock_send_email.assert_called_once_with(
            self.user,
            self.user.verification_code
        )

    def test_verify_user_email_verified(self):
        self.user.is_email_verified = True
        response = self.client.post(
            self.get_user_url("email_verify"),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email is already verified.", str(response.data))

    def test_verify_user_email_timeout(self):
        self.user.verification_code_timeout = (
            timezone.now() + datetime.timedelta(minutes=3)
        )
        response = self.client.post(
            self.get_user_url("email_verify"),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Email sending timeout is not over yet.",
            str(response.data)
        )

    def test_verify_user_email_entered_correct_code(self):
        self.user.verification_code = 120000
        self.user.save()
        response = self.client.patch(
            self.get_user_url("email_verify"),
            {
                "code": "120000"
            }
        )

        self.assertNotIn("error", str(response.data))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_verify_user_email_entered_incorrect_code(self):
        self.user.verification_code = 120000
        self.user.save()
        response = self.client.patch(
            self.get_user_url("email_verify"),
            {
                "code": "1200011"
            }
        )

        self.assertIn(
            "sure this value is less than or equal to 999999.",
            str(response.data)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            self.get_user_url("email_verify"),
            {
                "code": "130000"
            }
        )
        self.assertIn("Verification code does not match.", str(response.data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
