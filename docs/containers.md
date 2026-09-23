# Container Operations

The application image is built from the repository root. The final stage uses
the unprivileged `app` user and contains only the runtime dependencies copied
from the builder stage. Compose keeps the PostgreSQL data in the named
`postgres_data` volume and gates the web service on the database healthcheck.

## Local lifecycle

```bash
docker compose up -d --build
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py seed_demo_data
curl --fail http://localhost:8000/health
```

The default stack contains only the API and database. The optional
observability stack is enabled explicitly:

```bash
docker compose --profile observability up -d
```

Prometheus is available at `http://localhost:9090` and Grafana at
`http://localhost:3000`. Prometheus scrapes the API's `/metrics` endpoint over
the Compose service network.

## Diagnosis

Start with state and exit information, then inspect logs:

```bash
docker compose ps
docker inspect devops-isoko-web-1 --format '{{.State.Status}} exit={{.State.ExitCode}}'
docker compose logs web
docker compose logs db
```

An exited container indicates a process failure. A running container that fails
requests indicates a readiness or dependency failure; the web healthcheck and
database healthcheck make that distinction visible to Compose.

Do not use `docker compose down -v` as a routine cleanup command: it removes
the named database volume and its data.
