# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# системные зависимости (asyncpg/argon2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# зависимости проекта
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# исходники
COPY authentication ./authentication

# нерутовый пользователь
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# по умолчанию: прод-режим (см. compose для dev)
# Gunicorn + Uvicorn workers для продакшна
CMD ["python", "-m", "gunicorn", "authentication.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", "-w", "2", \
     "-b", "0.0.0.0:8000", "--timeout", "60"]
