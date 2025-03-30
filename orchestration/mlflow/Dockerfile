FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mlflow

# RUN pip install --no-cache-dir firebase-admin

WORKDIR /app

# COPY ./config /app/config

# Открытие порта для MLflow UI (default: 5000)
EXPOSE 5000

CMD ["mlflow", "ui"]