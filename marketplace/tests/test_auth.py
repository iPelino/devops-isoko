from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from marketplace.models import Profile


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer1", password="isoko-demo-1")

    def test_login_with_valid_credentials_returns_token(self):
        response = self.client.post(
            "/login", {"username": "buyer1", "password": "isoko-demo-1"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertEqual(
            response.json()["token"], Token.objects.get(user=self.user).key
        )

    def test_login_with_invalid_password_returns_401(self):
        response = self.client.post(
            "/login", {"username": "buyer1", "password": "wrong"}, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_login_with_unknown_username_returns_401(self):
        response = self.client.post(
            "/login", {"username": "nobody", "password": "whatever"}, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_new_user_gets_a_default_buyer_profile(self):
        self.assertEqual(self.user.profile.role, Profile.Role.BUYER)

    def test_orders_requires_authentication(self):
        response = self.client.get("/orders")

        self.assertEqual(response.status_code, 401)
