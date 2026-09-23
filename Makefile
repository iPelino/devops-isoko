.PHONY: lint format-check test coverage check run migrate seed smoke

lint:
	ruff check .

format-check:
	ruff format --check .

test:
	DJANGO_DEBUG=true DJANGO_SECRET_KEY="$${DJANGO_SECRET_KEY:-local-development-key}" python manage.py test marketplace

coverage:
	DJANGO_DEBUG=true DJANGO_SECRET_KEY="$${DJANGO_SECRET_KEY:-local-development-key}" \
		python -m coverage run manage.py test marketplace
	python -m coverage report --fail-under=70

check: lint format-check test

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate --noinput

seed:
	python manage.py seed_demo_data

smoke:
	curl --fail --silent http://127.0.0.1:8000/health
