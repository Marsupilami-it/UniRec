FROM ubuntu:latest
LABEL authors="ITon"

ENTRYPOINT ["top", "-b"]

FROM python:3.11
WORKDIR /app
COPY . .
RUN poetry install --no-dev
CMD ["python", "setup.py"]