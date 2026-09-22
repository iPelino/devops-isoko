from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from marketplace.models import Order, Product


class OrderTestsBase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer1", password="isoko-demo-1")
        self.product = Product.objects.create(
            name="Carrots", cooperative="Musanze Growers Cooperative", price_rwf=400
        )
        response = self.client.post(
            "/login", {"username": "buyer1", "password": "isoko-demo-1"}, format="json"
        )
        self.token = response.json()["token"]

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")


class PlaceOrderTests(OrderTestsBase):
    def test_place_order_returns_201_with_order_id(self):
        self.authenticate()

        response = self.client.post(
            "/orders", {"product_id": self.product.id, "quantity": 2}, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("order_id", response.json())
        order = Order.objects.get(id=response.json()["order_id"])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)

    def test_order_quantity_zero_is_rejected(self):
        self.authenticate()

        response = self.client.post(
            "/orders", {"product_id": self.product.id, "quantity": 0}, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_order_quantity_over_fifty_is_rejected(self):
        self.authenticate()

        response = self.client.post(
            "/orders", {"product_id": self.product.id, "quantity": 51}, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_order_for_nonexistent_product_is_rejected(self):
        self.authenticate()

        response = self.client.post(
            "/orders", {"product_id": 999999, "quantity": 1}, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_place_order_requires_authentication(self):
        response = self.client.post(
            "/orders", {"product_id": self.product.id, "quantity": 1}, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_order_is_always_tied_to_the_requesting_user(self):
        """Nothing in the request body can attribute the order to someone else."""
        self.authenticate()
        other_user = User.objects.create_user(username="someone-else", password="x")

        response = self.client.post(
            "/orders",
            {"product_id": self.product.id, "quantity": 1, "user": other_user.id},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(id=response.json()["order_id"])
        self.assertEqual(order.user, self.user)
