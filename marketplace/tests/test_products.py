from rest_framework.test import APITestCase

from marketplace.models import Product


class ProductSearchTests(APITestCase):
    def setUp(self):
        Product.objects.create(
            name="Tomatoes", cooperative="Musanze Growers Cooperative", price_rwf=500
        )
        Product.objects.create(
            name="Carrots", cooperative="Musanze Growers Cooperative", price_rwf=400
        )
        Product.objects.create(
            name="Onions", cooperative="Nyagatare Farmers Union", price_rwf=350
        )

    def test_search_by_name(self):
        response = self.client.get("/products/search", {"q": "tomato"})

        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 1)
        self.assertIn("tomato", results[0]["name"].lower())

    def test_search_by_name_is_case_insensitive(self):
        response = self.client.get("/products/search", {"q": "TOMATO"})

        self.assertEqual(len(response.json()), 1)

    def test_search_by_cooperative(self):
        response = self.client.get("/products/search", {"cooperative": "musanze"})

        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 2)
        self.assertTrue(all("musanze" in p["cooperative"].lower() for p in results))

    def test_search_with_no_params_returns_all(self):
        response = self.client.get("/products/search")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_search_does_not_require_authentication(self):
        response = self.client.get("/products/search")

        self.assertEqual(response.status_code, 200)


class ProductDetailTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Potatoes", cooperative="Nyagatare Farmers Union", price_rwf=300
        )

    def test_product_detail(self):
        response = self.client.get(f"/products/{self.product.id}")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["id"], self.product.id)
        self.assertEqual(body["price_rwf"], 300)
        self.assertEqual(body["cooperative"], "Nyagatare Farmers Union")

    def test_product_detail_not_found(self):
        response = self.client.get("/products/999999")

        self.assertEqual(response.status_code, 404)

    def test_product_detail_does_not_require_authentication(self):
        response = self.client.get(f"/products/{self.product.id}")

        self.assertEqual(response.status_code, 200)
