from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_health_returns_ok_without_auth(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
