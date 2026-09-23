from django.test import SimpleTestCase
from rest_framework.test import APITestCase


class MetricsTests(APITestCase):
    def test_metrics_returns_prometheus_content(self):
        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"isoko_http_requests_total", response.content)


class JsonLoggingTests(SimpleTestCase):
    def test_json_formatter_includes_message(self):
        import json
        import logging

        from isoko.logging import JsonFormatter

        record = logging.LogRecord(
            name="isoko.test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="test message",
            args=(),
            exc_info=None,
        )

        payload = json.loads(JsonFormatter().format(record))

        self.assertEqual(payload["message"], "test message")
