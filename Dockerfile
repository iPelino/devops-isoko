FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=app:app . /app

EXPOSE 8000

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "isoko.wsgi:application"]
