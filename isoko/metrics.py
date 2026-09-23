from prometheus_client import Counter, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    "isoko_http_requests_total",
    "Total HTTP requests handled by Isoko.",
    ["method", "status"],
)


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        record_request(request.method, response.status_code)
        return response


def record_request(method, status):
    REQUEST_COUNT.labels(method=method, status=str(status)).inc()


def render_metrics():
    return generate_latest(), CONTENT_TYPE_LATEST
