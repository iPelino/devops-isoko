# Isoko

Isoko ("market" in Kinyarwanda) is a produce marketplace API for farming
cooperatives around Kigali. Cooperatives list products; buyers search for
products, view product detail, place orders, and view their own order
history. This repo is a solo practice build of the Isoko Week 1 scenario
(see the issue tracker for the full scenario and business rules).

## Stack

- Python 3.12, Django 6.1, Django REST Framework
- Token authentication (`rest_framework.authtoken`)
- SQLite for local development
- `ruff` for linting/formatting, `pre-commit` to enforce it on every commit

## Running it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo_data   # creates buyer1/manager1 + sample products
python manage.py runserver
```

The API is then at `http://localhost:8000`. Try it:

```bash
curl http://localhost:8000/health
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
python manage.py test marketplace
```

## Contributing

See `CONTRIBUTING.md` for commit conventions and the PR workflow.
