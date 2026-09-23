# Isoko

Isoko ("market" in Kinyarwanda) is a produce marketplace API for farming
cooperatives around Kigali. Cooperatives list products; buyers search for
products, view product detail, place orders, and view their own order
history. This repo is a solo practice build of the Isoko Week 1 scenario
(see the issue tracker for the full scenario and business rules).

## Stack

- Python 3.12, Django 6.1, Django REST Framework
- Token authentication (`rest_framework.authtoken`)
- PostgreSQL 16
- `ruff` for linting/formatting, `pre-commit` to enforce it on every commit

## Running it locally

```bash
cp .env.example .env
docker compose up -d
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_demo_data
```

The API is then at `http://localhost:8000`. Try it:

```bash
docker compose logs -f web
```

```bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
curl "http://localhost:8000/products/search?q=tomato"

TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "buyer1", "password": "isoko-demo-1"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

curl http://localhost:8000/orders -H "Authorization: Token $TOKEN"
```

## Endpoints

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/health` | none | liveness check |
| POST | `/login` | none | username/password -> token |
| GET | `/products/search` | none | filter by `q` and/or `cooperative` |
| GET | `/products/<id>` | none | product detail |
| POST | `/orders` | token | place an order (quantity 1-50) |
| GET | `/orders` | token | the caller's own order history |

## Testing

```bash
make check
make coverage
```

For container operations and the optional Prometheus/Grafana profile, see
[`docs/containers.md`](docs/containers.md).

## Contributing

See `CONTRIBUTING.md` for commit conventions and the PR workflow.
