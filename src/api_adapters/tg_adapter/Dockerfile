FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
VOLUME /app

COPY src.py requirements.txt .env ./

RUN apt-get update && python3 -m pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt
